#!/usr/bin/python

from subprocess import call
from ctypes import *

import tempfile

import eel_instr
import eel_cur_ctx
from eel_eval import eval
from eel_context import Context

def compile(exp):
    from eel_eval import eval
    import eel_instr as i
    if isinstance(exp, i.BCall):
        if isinstance(exp[0], i.PCall):
            if exp[0][0] == "if":
                ret = "if"
                ret += "("
                ret += compile(exp[0][1])
                ret += ")"
                ret += "{"
                ret += compile(exp[1:])
                ret += "}"
                return ret
            if exp[0][0] == "_":
                ret = str(exp[0][1])
                for e in exp[1:]:
                    ret += " " + str(compile(e))
                return ret
        return str(exp)
    elif isinstance(exp, i.PCall):
        f = eval(exp[0])
        ret = f.compile_call(exp[1:])
        return ret
    elif isinstance(exp, list):
        ret = ""
        for e in exp:
            ret += compile(e) + ";"
        return ret
    return str(exp)

d = tempfile.mkdtemp()

ld_flags = []

def mkCFunc(sym, restype, params, exp):
    import eel_cur_ctx
    test  = "#include <Python.h>\n"
    test += str(restype)
    test += " "
    test += str(sym)
    test += "("
    for p in params:
        test += p.type + " " + p
    test += ")"
    test += "{"
    test += compile(exp)
    test += "}"

    print(eel_cur_ctx.cur_ctx)
    print(test)
    f = open(d+"/"+str(sym)+".c", "w+")
    f.write(str(test))
    f.close()

    cmd  = ["gcc", "-shared", "-fPIC", d+"/"+str(sym)+".c", "-o", d+"/"+str(sym)+".so"]
    cmd += ["-I/usr/include/python2.7"]
    cmd += ld_flags
    cmd += ["-Wno-implicit-function-declaration"]
    call(cmd)
    ld_flags.append(d+"/"+str(sym)+".so")

    test_so = CDLL(d+"/"+str(sym)+".so")

    return test_so[sym]

class Func(object):
    class Return(object):
        def __init__(self, val):
            self.val = val
    def __init__(self, sym, restype, params_types, params, exp, ctx):
        self.params = map(lambda pt: eel_instr.Symbol(pt[0], pt[1]), zip(params, params_types))
        self.exp = exp
        self.ctx = ctx
        self.sym = sym
        self.restype = restype
        self.params_types = params_types
        tmp_ctx = eel_cur_ctx.cur_ctx
        eel_cur_ctx.cur_ctx = Context(map(lambda p: (p, None), self.params), ctx)
        self.cfunc = mkCFunc(self.sym, self.restype, self.params, self.exp)
        eel_cur_ctx.cur_ctx = tmp_ctx
    def compile_call(self, *args):
        ret = str(self.sym)
        ret += "("
        for a in args[0]:
            ret += str(compile(a))
        ret += ")"
        return ret
    def __call__(self, *args):
        return self.cfunc(*args)
    def prev_call(self, *args):
        prev_ctx = eel_cur_ctx.cur_ctx
        eel_cur_ctx.cur_ctx =  Context(zip(self.params, args), self.ctx)
        ret = None
        for e in self.exp:
            tmp = eval(e)
            if isinstance(tmp, Func.Return):
                ret = tmp.val
                break
        eel_cur_ctx.cur_ctx = prev_ctx
        return ret

class BOp(object):
    def __init__(self, sym, func):
        self.func = func
        self.sym = sym
    def compile_call(self, *args):
        ret = str(compile(args[0][0]))
        for a in args[0][1:]:
            ret += str(self.sym)
            ret += str(compile(a))
        return ret
    def __call__(self, *args):
        return self.func(*args)

class PyFunc(object):
    def __init__(self, sym, func):
        self.func = func
        self.sym = sym
    def compile_call(self, *args):
        args_str = "("
        args_vals = []
        for a in args[0]:
            if isinstance(a, int):
                args_str += "i"
                args_vals.append(str(a))
            if isinstance(a, eel_instr.Symbol):
                ctx = eel_cur_ctx.cur_ctx.search(a)
                for v in ctx.keys():
                    if v == a:
                        args_vals.append(a)
                        if v.type == "int":
                            args_str += "i"

        args_str += ")"
        ret  = '{'
        ret += 'PyObject* arglist = 0;'
        ret += 'PyObject* result = 0;'
        ret += 'arglist = Py_BuildValue("'+args_str+'", '+','.join(args_vals)+');'
        ret += 'PyGILState_STATE gstate;'
        ret += 'gstate = PyGILState_Ensure();'
        ret += 'result = PyEval_CallObject(((PyObject*)'+hex(id(self.func))+'), arglist);'
        ret += 'PyGILState_Release(gstate);'
        ret += 'Py_DECREF(arglist);'
        ret += '}'
        return ret
    def __call__(self, *args):
        return self.func(*args)

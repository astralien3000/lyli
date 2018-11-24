#!/usr/bin/python

from subprocess import call
from ctypes import *

import tempfile

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
        f.build()
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

def mkCFunc(sym, restype, params_types, params, exp):
    params = zip(params_types, params)
    test = str(restype)
    test += " "
    test += str(sym)
    test += "("
    for p in params:
        test += p[0] + " " + p[1]
    test += ")"
    test += "{"
    test += compile(exp)
    test += "}"

    f = open(d+"/"+str(sym)+".c", "w+")
    f.write(str(test))
    f.close()

    cmd  = ["gcc", "-shared", "-fPIC", d+"/"+str(sym)+".c", "-o", d+"/"+str(sym)+".so"]
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
        self.params = params
        self.exp = exp
        self.ctx = ctx
        self.sym = sym
        self.restype = restype
        self.params_types = params_types
        self.cfunc = None
    def compile_call(self, *args):
        ret = str(self.sym)
        ret += "("
        for a in args[0]:
            ret += str(compile(a))
        ret += ")"
        return ret
    def build(self):
        if not self.cfunc:
            self.cfunc = mkCFunc(self.sym, self.restype, self.params_types, self.params, self.exp)
    def __call__(self, *args):
        if not self.cfunc:
            self.cfunc = mkCFunc(self.sym, self.restype, self.params_types, self.params, self.exp)
        return self.cfunc(*args)
    def prev_call(self, *args):
        from eel_eval import eval
        from eel_context import Context
        import eel_cur_ctx
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
    def build(self):
        pass
    def __call__(self, *args):
        return self.func(*args)

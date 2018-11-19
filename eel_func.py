#!/usr/bin/python

from cgen import *
from subprocess import call
from ctypes import *

import tempfile

def compile(exp):
    import eel_instr as i
    if isinstance(exp, i.BCall):
        if isinstance(exp[0], i.PCall):
            if exp[0][0] == "if":
                return If(compile(exp[0][1]), Block(compile(exp[1:])))
            if exp[0][0] == "_":
                ret = str(exp[0][1])
                for e in exp[1:]:
                    ret += " " + str(compile(e))
                return Statement(ret)
        return Line(str(exp))
    elif isinstance(exp, i.PCall):
        if exp[0] == "==":
            return Line(compile(exp[1]) + " == " + compile(exp[2]))
        if exp[0] == "<":
            return Line(compile(exp[1]) + " < " + compile(exp[2]))
        if exp[0] == "+":
            return Line(str(compile(exp[1])) + " + " + str(compile(exp[2])))
        if exp[0] == "-":
            return Line(str(compile(exp[1])) + " - " + str(compile(exp[2])))
        ret = str(exp[0])
        ret += "("
        ret += str(compile(exp[1]))
        for e in exp[2:]:
            ret += ", " + str(compile(e))
        ret += ")"
        return Line(str(ret))
    elif isinstance(exp, list):
        ret = list()
        for e in exp:
            ret.append(compile(e))
        return Block(ret)
    return str(exp)

d = tempfile.mkdtemp()

def mkCFunc(sym, restype, params_types, params, exp):
    params = map(lambda (t, s): Value(t,s), zip(params_types, params))
    body = compile(exp)
    test = FunctionBody(
        FunctionDeclaration(Value(str(restype), sym), params),
        body
    )

    print(test)
    f = open(d+"/"+str(sym)+".c", "w+")
    f.write(str(test))
    f.close()

    call(["gcc", "-shared", "-fPIC", d+"/"+str(sym)+".c", "-o", d+"/"+str(sym)+".so"])

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
        self.cfunc = mkCFunc(sym, restype, params_types, params, exp)
    def __call__(self, *args):
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

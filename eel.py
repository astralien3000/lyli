#!/usr/bin/python3
# coding: UTF-8

import lark

from eel.instr import *
from eel.transformer import *
from eel.context import *
from eel.func import *
from eel.eval import *
import eel.cur_ctx

eel.parser = lark.Lark(open("eel.lark", "r", encoding="utf-8"), parser="lalr", transformer=EelTransformer())

def global_context(self):
    def _print(args):
        print(args)
    def _defint(*args):
        if len(args) == 3 and args[1] == "=":
            eel.cur_ctx.cur_ctx.update({args[0] : args[2]})
        elif len(args) == 1:
            eel.cur_ctx.cur_ctx.update({args[0] : 0})
        else:
            raise Exception("WRONG DEFINE FORM")
        return None
    def _fn(*args):
        if isinstance(args[-1], list):
            params = list(map(lambda x: x[1], args[-1][0][1:]))
            params_types = list(map(lambda x: x[0][1], args[-1][0][1:]))
            eel.cur_ctx.cur_ctx.update({
                args[-1][0][0] : Func(args[-1][0][0], args[-2], params_types, params, args[-1][1:], eel.cur_ctx.cur_ctx)
            })
        else:
            raise Exception("WRONG DEFINE FORM")
    def _if(arg):
        if arg:
            return lambda a: eval(a)
        return lambda a: None
    def _ret(arg):
        return Func.Return(eval(arg))
    def _import(arg):
        import importlib
        mod = importlib.import_module(arg)
        eel.cur_ctx.cur_ctx.update(vars(mod))
        return None
    def _(arg):
        return arg
    def _defstruct(*args):
        import ctypes
        name = args[0][0]
        members = args[0][1:]
        fields = []
        for m in members:
            if(m[0][1] == "int"):
                fields.append((m[1], ctypes.c_int))
        class DefStruct(ctypes.Structure):
            _fields_ = fields
        def _def(*args):
            if len(args) == 1:
                eel.cur_ctx.cur_ctx.update({args[0] : DefStruct()})
            else:
                raise Exception("WRONG DEFINE FORM")
            return None
        eel.cur_ctx.cur_ctx.update({
            name : _def
        })
        def _get(memb):
            return lambda *args: getattr(args[0], memb)
        def _set(memb):
            return lambda *args: setattr(args[0], memb, args[1])
        for m in members:
            eel.cur_ctx.cur_ctx.update({
                "get_" + m[1] : _get(m[1]),
                "set_" + m[1] : _set(m[1]),
            })
    ret = Context({
        "_" : _,
        "print" : PyFunc("print", _print),
        "int" : _defint,
        "fn" : _fn,
        "if" : _if,
        "return" : _ret,
        "import" : _import,
        "struct" : _defstruct,
    }, self)
    import operator as op
    ret.update({
        "+" : BOp("+", op.add),
        "-" : BOp("-", op.sub),
        "*" : BOp("*", op.mul),
        "!" : BOp("!", op.not_),
        "~" : BOp("~", op.inv),
        "<" : BOp("<", op.lt),
        ">" : BOp(">", op.gt),
        "<=" : BOp("<=", op.le),
        ">=" : BOp(">=", op.ge),
        "==" : BOp("==", op.eq),
        "!=" : BOp("!=", op.ne),
        "||" : BOp("||", op.or_),
    })
    return ret

eel.cur_ctx.cur_ctx = global_context(eel.cur_ctx.cur_ctx)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            ast = eel.parser.parse(f.read())
            print(ast)
            for e in ast:
                res = eval(e)
                if res: print(res)
    
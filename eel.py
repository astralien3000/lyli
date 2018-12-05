#!/usr/bin/python
# coding: UTF-8

import lark

from eel_instr import *
from eel_transformer import *
from eel_context import *
from eel_func import *
from eel_eval import *
import eel_cur_ctx

eel_parser = lark.Lark.open("eel.lark", parser="lalr", transformer=EelTransformer())

def global_context(self):
    def _print(args):
        print(args)
    def _def(*args):
        if isinstance(args[-1], list) and args[-1][0] == "=":
            eel_cur_ctx.cur_ctx.update({args[-1][1] : args[-1][2]})
        else:
            raise Exception("WRONG DEFINE FORM")
        return None
    def _fn(*args):
        if isinstance(args[-1], list):
            params = map(lambda x: x[1], args[-1][0][1:])
            params_types = map(lambda x: x[0][1], args[-1][0][1:])
            eel_cur_ctx.cur_ctx.update({
                args[-1][0][0] : Func(args[-1][0][0], args[-2], params_types, params, args[-1][1:], eel_cur_ctx.cur_ctx)
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
        eel_cur_ctx.cur_ctx.update(vars(mod))
        return None
    def _(arg):
        return arg
    ret = Context({
        "_" : _,
        "print" : PyFunc("print", _print),
        "int" : _def,
        "fn" : _fn,
        "if" : _if,
        "return" : _ret,
        "import" : _import,
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

eel_cur_ctx.cur_ctx = global_context(eel_cur_ctx.cur_ctx)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            ast = eel_parser.parse(f.read())
            print ast
            for e in ast:
                res = eval(e)
                if res: print res
    
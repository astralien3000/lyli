#!/usr/bin/python3
# coding: UTF-8

import lark

from eel.ast import *
from eel.transformer import *
from eel.context import *
from eel.func import *
from eel.eval import *
from eel import prelude
import eel

eel.parser = lark.Lark(open("eel.lark", "r", encoding="utf-8"), parser="lalr", transformer=EelTransformer())

eel.context.cur_ctx = Context({}, eel.prelude.prelude_ctx)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            ast = eel.parser.parse(f.read())
            print("---------------- AST BEG ----------------")
            print(ast)
            print("---------------- AST END ----------------")
            res = eval_one(ast)
            if res: print(res)

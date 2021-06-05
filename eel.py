#!/usr/bin/python3
# coding: UTF-8

import lark

import eel

eel.parser = lark.Lark(eel.grammar.grammar, parser="lalr", transformer=eel.transformer.Transformer())

eel.context.cur_ctx = eel.context.Context({}, eel.prelude.prelude_ctx)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            ast = eel.parser.parse(f.read())
            print("---------------- AST BEG ----------------")
            print(ast)
            print("---------------- AST END ----------------")
            res = eel.eval.eval_one(ast)
            if res: print(res)

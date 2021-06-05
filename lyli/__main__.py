import lark

import eval
import grammar
import transformer
import prelude
import context

parser = lark.Lark(grammar.grammar, parser="lalr", transformer=transformer.Transformer())

context.cur_ctx = context.Context({}, prelude.prelude_ctx)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            expr = parser.parse(f.read())
            print("---------------- ast BEG ----------------")
            print(expr)
            print("---------------- ast END ----------------")
            res = eval.eval_one(expr)
            if res: print(res)

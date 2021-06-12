import lark

import lyli.eval as eval
import lyli.grammar as grammar
import lyli.transformer as transformer
import lyli.prelude as prelude
import lyli.context as context
import lyli.compile as compile

parser = lark.Lark(grammar.grammar, parser="lalr", transformer=transformer.Transformer())

context.cur_ctx = context.Context({}, prelude.prelude_ctx)

def main():
  import sys
  if len(sys.argv) == 1:
    while True:
      raw = input(">")
      expr = parser.parse(raw)
      res = eval.eval_one(expr)
      if res: print(res)
  elif len(sys.argv) == 2:
    with open(sys.argv[1], "r") as f:
      expr = parser.parse(f.read())
      print("---------------- ast BEG ----------------")
      print(expr)
      print("---------------- ast END ----------------")
      res = eval.eval_one(expr)
      if context.cur_ctx.exists("main"):
        print("main found ! compile...")
        compile.compile_main(context.cur_ctx["main"])
        

if __name__ == "__main__":
  main()
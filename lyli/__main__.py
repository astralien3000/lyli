import lark
import sys

import lyli.eval as eval
import lyli.grammar as grammar
import lyli.transformer as transformer
import lyli.prelude as prelude
import lyli.context as context
import lyli.compile as compile

parser = lark.Lark(grammar.grammar)
trans = transformer.Transformer()

context.cur_ctx = context.Context({}, prelude.prelude_ctx)


def main(argv=sys.argv[1:]):
  if len(argv) == 0:
    while True:
      raw = input(">")
      expr = parser.parse(raw)
      res = eval.eval_one(expr)
      if res: print(res)
  elif len(argv) == 1:
    with open(argv[0], "r") as f:
      code = f.read()
      raw = parser.parse(code)
      expr = trans.transform(raw)
      print("---------------- code BEG ----------------")
      print(code)
      print("---------------- code END ----------------")
      # print("---------------- raw ast BEG ----------------")
      # print(raw)
      # print("---------------- raw ast END ----------------")
      print("---------------- ast BEG ----------------")
      print(expr)
      print("---------------- ast END ----------------")
      """res = eval.eval_one(expr)
      if "main" in context.cur_ctx:
        print("main found ! compile...")
        compile.compile_main(context.cur_ctx["main"])"""


if __name__ == "__main__":
  main()

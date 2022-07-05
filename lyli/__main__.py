import lark
import sys
import os
import re

import lyli.eval as eval
import lyli.prelude as prelude
import lyli.context as context
import lyli.compile as compile
import lyli.parse as parse


context.cur_ctx = context.Context({}, prelude.prelude_ctx)


def main(argv=sys.argv[1:]):
  cur_ctx = context.Context(prelude.prelude_ctx)
  if len(argv) == 0:
    while True:
      code = input(">")
      expr = parse.parse(code)
      print(expr)
      cur_ctx, res = eval.eval(cur_ctx, expr)
      if res is not None: print(res)
  elif len(argv) == 1:
    expr = parse.parse_file(argv[0])
    print("---------------- ast BEG ----------------")
    print(expr)
    print("---------------- ast END ----------------")
    cur_ctx, res = eval.eval(cur_ctx, expr)
    if "main" in context.cur_ctx:
      print("main found ! compile...")
      compile.compile_main(context.cur_ctx["main"])


if __name__ == "__main__":
  main()

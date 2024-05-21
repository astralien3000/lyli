import sys
import argparse

import lyli.eval as eval
import lyli.prelude as prelude
import lyli.context as context
import lyli.ast as ast
import lyli.compile.js as js


def main(argv=sys.argv[1:]):
  args_parser = argparse.ArgumentParser(
    description="lyli interpreter",
  )
  args_parser.add_argument(
    "source_file",
    type=str,
    nargs="?",
    help="a lyli source file",
  )
  args_parser.add_argument(
    "-i", "--idir",
    type=str,
    action="append",
    help="import dir",
  )
  args = args_parser.parse_args(argv)
  cur_ctx = context.Context(
    parent=prelude.prelude_ctx,
    data={
      "IDIR": args.idir,
    }
  )
  if args.source_file is None:
    while True:
      code = input(">")
      expr = ast.parse(code)
      print(expr)
      res = eval.eval(expr, cur_ctx)
      if res is not None: print(res)
      # print(js.compile(expr))
  else:
    with open(args.source_file) as f:
      expr = ast.parse(f.read())
    print("---------------- ast BEG ----------------")
    print(expr)
    print("---------------- ast END ----------------")
    print("---------------- unparse BEG ----------------")
    print(ast.unparse(expr))
    print("---------------- unparse END ----------------")
    res = eval.eval(expr, cur_ctx)


if __name__ == "__main__":
  main()

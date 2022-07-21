import sys
import argparse

import lyli.eval as eval
import lyli.prelude as prelude
import lyli.context as context
import lyli.parse as parse


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
      expr = parse.parse(code)
      print(expr)
      cur_ctx, res = eval.eval(cur_ctx, expr)
      if res is not None: print(res)
  else:
    expr = parse.parse_file(args.source_file)
    print("---------------- ast BEG ----------------")
    print(expr)
    print("---------------- ast END ----------------")
    cur_ctx, res = eval.eval(cur_ctx, expr)


if __name__ == "__main__":
  main()

from genericpath import exists
import lyli.eval as eval
import lyli.parse as parse
import lyli.prelude as prelude

import os


def _import(ctx, filename_expr):
  ctx, filename = eval.eval(ctx, filename_expr)
  idir = ctx["IDIR"]
  for dir in idir:
    source_file = os.path.join(dir, filename)
    if os.path.exists(source_file):
      expr = parse.parse_file(source_file)
      new_ctx, ret = eval.eval(ctx, expr)
      return new_ctx, ret
  raise Exception(f"source file not found : {filename}")

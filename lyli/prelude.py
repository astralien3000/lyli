import lyli.context as context
import lyli.func as func
import lyli.eval as eval


def _file(ctx, *args):
  ret = None
  for arg in args:
    ctx, ret = eval.eval(ctx, arg)
  return ctx, ret


prelude_ctx = context.Context({
    "print": func.PyFunc(print),
    "file": func.PyMacro(_file),
})

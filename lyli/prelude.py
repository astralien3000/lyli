import lyli.context as context
import lyli.func as func
import lyli.eval as eval
import lyli.ast as ast


def _file(ctx, *args):
  ret = None
  for arg in args:
    ctx, ret = eval.eval(ctx, arg)
  return ctx, ret


def _stmt(ctx, *args):
  return eval.eval(
    ctx,
    ast.Call(
      ast.Symbol(f"stmt.{args[0]}"),
      *args[1:],
    )
  )


def _let(ctx, *args):
  new_ctx = context.Context(ctx, { str(args[0]): args[2] })
  return new_ctx, None


prelude_ctx = context.Context({
  "file": func.PyMacro(_file),
  "stmt": func.PyMacro(_stmt),

  "stmt.let": func.PyMacro(_let),

  "print": func.PyFunc(print),
  "stmt.print": func.PyFunc(print),
})

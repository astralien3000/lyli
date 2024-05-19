import lyli.ast._ast as _ast
import lyli.context as context
import lyli.func as func

def eval(ctx, expr):
  if isinstance(expr, _ast.Symbol):
    return ctx, ctx[expr.name]
  elif isinstance(expr, _ast.Atomic):
    return ctx, expr.value
  elif isinstance(expr, _ast.Call):
    _, f = eval(ctx, expr[0])
    if isinstance(f, func.Func):
      args = expr[1:]
      return f(ctx, *args)
    else:
      raise TypeError(f"not a Func : {expr[0]}")
  else:
    raise TypeError(f"not valid : {type(expr)} ({expr})")

import lyli.ast as ast
import lyli.context as context
import lyli.func as func

def eval_one(x):
  #print("EVAL : " + str(x))
  if isinstance(x, ast.Symbol):
    return context.cur_ctx[str(x)]
  elif isinstance(x, ast.Atomic):
    return x
  elif isinstance(x, ast.Call):
    f = eval_one(x[0])
    if isinstance(f, func.Func):
      args = x[1:]
      return f(*args)
    else:
      raise TypeError("not a Func : " + str(x[0]))
  elif isinstance(x, ast.Expr):
    raise TypeError("not (yet) supported : " + str(type(x)) + " (" + str(x) + ")")
  else:
    raise TypeError("not valid : " + str(type(x)) + " (" + str(x) + ")")

def eval_all(*args):
  ret = None
  for x in args:
    if x:
      ret = eval_one(x)
  return ret

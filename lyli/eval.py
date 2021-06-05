import expr_tree
import context
import func

def eval_one(x):
  if isinstance(x, expr_tree.Symbol):
    return context.cur_ctx[str(x)]
  elif isinstance(x, expr_tree.Atomic):
    return x.val
  elif isinstance(x, expr_tree.Call):
    f = eval_one(x[0])
    if isinstance(f, func.Func):
      args = x[1:]
      return f(*args)
    else:
      raise TypeError("not a Func : " + str(x[0]))
  elif isinstance(x, expr_tree.Expr):
    raise TypeError("not (yet) supported : " + str(type(x)) + " (" + str(x) + ")")
  else:
    return x

def eval_all(*args):
  ret = None
  for x in args:
    ret = eval_one(x)
  return ret

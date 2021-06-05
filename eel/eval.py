from .ast import Symbol,Atomic,Call
from . import context
from . import func

def eval_one(x):
  if isinstance(x, Symbol):
    return context.cur_ctx[str(x)]
  elif isinstance(x, Atomic):
    return x.val
  elif isinstance(x, Call):
    f = eval_one(x[0])
    if isinstance(f, func.Func):
      args = x[1:]
      return f(*args)
    else:
      raise TypeError("ERROR : not a Proc " + str(x[0]))
  else:
    #print("WARNING (should not happen ?) : " + str(x))
    return x

def eval_all(*args):
  ret = None
  for x in args:
    ret = eval_one(x)
  return ret

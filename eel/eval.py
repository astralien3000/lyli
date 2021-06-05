from .ast import Symbol,Atomic,Call
from . import context
from . import func

def eval_one(x):
  if isinstance(x, Symbol):
    return context.cur_ctx[str(x)]
  elif isinstance(x, Atomic):
    return x.val
  elif isinstance(x, Call):
    proc = eval_one(x[0])
    if isinstance(proc, func.Macro):
      args = x[1:]
      return proc(*args)
    else:
      args = [eval_one(exp) for exp in x[1:]]
      return proc(*args)
  else:
    #print("WARNING (should not happen ?) : " + str(x))
    return x

def eval_all(*args):
  ret = None
  for x in args:
    ret = eval_one(x)
  return ret

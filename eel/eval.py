from .instr import *
from .context import *
from . import context

def eval(x):
    if isinstance(x, Symbol):
        return context.cur_ctx[x]
    elif not isinstance(x, list):
        return x
    else:
        proc = eval(x[0])
        if isinstance(x, BCall):
            args = x[1:]
            return proc(*args)
        else:
            args = [eval(exp) for exp in x[1:]]
            return proc(*args)

from .instr import *
from .context import *
from . import context
from . import func

def eval(x):
    if isinstance(x, Symbol):
        return context.cur_ctx[x]
    elif not isinstance(x, list):
        return x
    else:
        proc = eval(x[0])
        if isinstance(proc, func.Macro):
            args = x[1:]
            return proc(*args)
        else:
            args = [eval(exp) for exp in x[1:]]
            return proc(*args)

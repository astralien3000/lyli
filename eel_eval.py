from eel_instr import *
from eel_context import *
import eel_cur_ctx

def eval(x):
    if isinstance(x, Symbol):
        return eel_cur_ctx.cur_ctx[x]
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

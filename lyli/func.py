import lyli.ast as ast
import lyli.context as context
import lyli.eval as eval

class Func:
    class Return(object):
        def __init__(self, val):
            self.val = val
    def __init__(self, restype, params_types, params, exp, ctx):
        self.params = params
        self.exp = exp
        self.ctx = ctx
        self.restype = restype
        self.params_types = params_types
    def __call__(self, *_args):
        args = [eval.eval_one(exp) for exp in _args]
        prev_ctx = context.cur_ctx
        context.cur_ctx =  context.Context(zip(map(lambda x: str(x), self.params), args), self.ctx)
        ret = None
        for e in self.exp:
            tmp = eval.eval_one(e)
            if isinstance(tmp, Func.Return):
                ret = tmp.val
                break
        context.cur_ctx = prev_ctx
        return ret
    def __str__(self):
        ret = "[fn "
        ret += str(self.params) + " -> "
        ret += str(self.restype) + " \n"
        for e in self.exp:
          ret += str(e) + "\n"
        ret += "]"
        return ret

class BOp(Func):
    def __init__(self, func):
        self.func = func
    def __call__(self, *_args):
        args = [eval.eval_one(exp) for exp in _args]
        return self.func(*args)

class PyFunc(Func):
    def __init__(self, func):
        self.func = func
    def __call__(self, *_args):
        args = [eval.eval_one(exp) for exp in _args]
        return self.func(*args)
    def __str__(self):
        ret = "[pyfn "
        ret += str(self.func)
        ret += "]"
        return ret

class Macro(Func):
    def __init__(self, params, exp):
        self.params = params
        self.exp = ast.Call([ast.Symbol("$")] + exp)
    def __call__(self, *args):
        context.cur_ctx.update(zip(map(lambda x: str(x), self.params), args))
        ret = eval.eval_one(self.exp)
        return ret
      
class PyMacro(Macro):
    def __init__(self, func):
        self.func = func
    def __call__(self, *args):
        return self.func(*args)
  
import lyli.ast as ast
import lyli.context as context
import lyli.eval as eval


class Func:
  pass


class Macro(Func):
  pass


class LyliFunc(Func):

  class Return(object):
    def __init__(self, val):
      self.val = val

  def __init__(self, restype, params_types, params, exp, func_ctx):
    self.params = params
    self.exp = exp
    self.func_ctx = func_ctx
    self.restype = restype
    self.params_types = params_types

  def __call__(self, ctx, *args):
    args = [eval.eval(ctx, arg)[1] for arg in args]
    exec_ctx = context.Context(self.func_ctx, {
      k: v
      for k, v in zip(map(lambda x: str(x), self.params), args)
    })
    ret = None
    for e in self.exp:
      _, tmp = eval.eval(exec_ctx, e)
      if isinstance(tmp, LyliFunc.Return):
        ret = tmp.val
        break
    return ctx, ret

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

  def __call__(self, ctx, a, b):
    _, a = eval.eval(ctx, a)
    _, b = eval.eval(ctx, b)
    ret = self.func(a, b)
    return ctx, ret


class PyFunc(Func):

  def __init__(self, func):
    self.func = func

  def __call__(self, ctx, *args):
    args = [eval.eval(ctx, arg)[1] for arg in args]
    return ctx, self.func(*args)

  def __str__(self):
    ret = "[pyfn "
    ret += str(self.func)
    ret += "]"
    return ret


class LyliMacro(Macro):

  def __init__(self, params, exp):
    self.params = params
    self.exp = ast.Call([ast.Symbol("body")] + exp)

  def __call__(self, ctx, *args):
    exec_ctx = context.Context(ctx, {
      k: v
      for k, v in zip(map(lambda x: str(x), self.params), args)
    })
    _, ret = eval.eval(exec_ctx, self.exp)
    return exec_ctx, ret


class PyMacro(Macro):

  def __init__(self, func):
    self.func = func

  def __call__(self, ctx, *args):
    return self.func(ctx, *args)

  def __str__(self):
    ret = "[pymacro "
    ret += str(self.func)
    ret += "]"
    return ret

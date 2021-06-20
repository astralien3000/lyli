import lyli.ast as ast
import lyli.context as context
import lyli.eval as eval
import lyli.type

def typeof(arg):
  if isinstance(arg, ast.Symbol):
    return context.cur_ctx[context.cur_ctx[str(arg)].type]
  elif isinstance(arg, ast.Atomic):
    return context.cur_ctx[arg.type]
  else:
    print(arg)
    raise "ERR"

class Func(lyli.type.Object):
  class Return(object):
    def __init__(self, val):
      self.val = val
  def __init__(self, restype, params_types, params, exp, ctx):
    self.params = params
    self.exp = exp
    self.ctx = ctx
    self.restype = restype
    self.params_types = params_types
    lyli.type.Object.__init__(self, self, "func.Func")
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
    lyli.type.Object.__init__(self, self, "func.BOp")
  def __call__(self, *_args):
    args = [eval.eval_one(exp) for exp in _args]
    return self.func(*args)

class PyFunc(Func):
  def __init__(self, func):
    self.func = func
    print(func)
    print(func.__code__.co_argcount)
    lyli.type.Object.__init__(self, self, "func.PyFunc")
  def __call__(self, *_args):
    args = [eval.eval_one(exp) for exp in _args]
    return self.func(*args)
  def __str__(self):
    ret = "[pyfn "
    ret += str(self.func)
    ret += "]"
    return ret

class TypedPyFunc(PyFunc):
  def __init__(self, params_types, func):
    self.func = func
    self.params_types = params_types
    assert(len(self.params_types) == func.__code__.co_argcount)
    lyli.type.Object.__init__(self, self, "func.PyFunc")
  def match(self, *_args):
    return all([a == b for (a, b) in zip([typeof(x).val for x in _args], self.params_types)])
  def __call__(self, *_args):
    assert(len(self.params_types) == len(_args))
    assert(self.match(*_args))
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
    lyli.type.Object.__init__(self, self, "func.Macro")
  def __call__(self, *args):
    context.cur_ctx.update(zip(map(lambda x: str(x), self.params), args))
    ret = eval.eval_one(self.exp)
    return ret
    
class PyMacro(Macro):
  def __init__(self, func):
    self.func = func
    lyli.type.Object.__init__(self, self, "func.PyMacro")
  def __call__(self, *args):
    return self.func(*args)

class PolymorphicFunc(Func):
  def __init__(self, funcs):
    self.funcs = funcs
    lyli.type.Object.__init__(self, self, "func.PolymorphicFunc")
  def __call__(self, *args):
    candidates = list(filter(lambda f: f.match(*args), self.funcs))
    if(len(candidates) == 1):
      return candidates[0](*args)
    else:
      print([typeof(x).val for x in args])
      raise "TypeError"

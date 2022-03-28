import lyli.ast as ast
import lyli.context as context
import lyli.eval as eval
import lyli.object

def typeof(arg):
  #print("typeof : " + str(arg))
  if isinstance(arg.typ, lyli.object.Object):
    return arg.typ
  else:
    return context.cur_ctx[arg.typ]

def args_types(*args):
  #print("args_types : " + str(args))
  return [typeof(x) for x in args]

def match_types(a, b):
  #print("match_types : " + str((str(a),str(b))))
  if isinstance(a, lyli.object.Object):
    return match_types(a.val, b)
  elif isinstance(b, lyli.object.Object):
    return match_types(a, b.val)
  elif callable(b):
    return b(a)
  else:
    return a == b

class Func(lyli.object.Object):
  class Return(object):
    def __init__(self, val):
      self.val = val
  def __init__(self, restype, params_types, params, exp, func_ctx):
    self.params = params
    self.exp = exp
    self.func_ctx = func_ctx
    self.restype = restype
    self.params_types = params_types
    lyli.object.Object.__init__(self, self, "func.Func")
  def __call__(self, *_args):
    #print("FUNC : " + str(self) + str(_args))
    args = [eval.eval_one(exp) for exp in _args]
    prev_ctx = context.cur_ctx
    context.cur_ctx =  context.Context(zip(map(lambda x: str(x), self.params), args), self.func_ctx)
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

class Func2(Func):
  class Return(object):
    def __init__(self, val):
      self.val = val
  def __init__(self, restype, params_types, params, exp, func_ctx):
    self.params = params
    self.exp = exp
    self.func_ctx = func_ctx
    self.restype = restype
    self.params_types = params_types
    lyli.object.Object.__init__(self, self, "func.Func")
  def __call__(self, *_args):
    #print("FUNC : " + str(self) + str(_args))
    args = [eval.eval_one(exp) for exp in _args]
    prev_ctx = context.cur_ctx
    context.cur_ctx =  context.Context(zip(map(lambda x: str(x), self.params), args), self.func_ctx)
    ret = eval.eval_one(self.exp)
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
  def __init__(self, func, ret = None):
    self.func = func
    self.ret = ret
    lyli.object.Object.__init__(self, self, "func.BOp")
  def match(self, *args):
    return True
  def __call__(self, a, b):
    aa = eval.eval_one(a)
    bb = eval.eval_one(b)
    #print("a = " + str(a))
    #print("b = " + str(b))
    #print("aa = " + str(aa))
    #print("bb = " + str(bb))
    assert(aa.typ == bb.typ)
    ret = self.func(aa.val, bb.val)
    return lyli.object.Object(ret, self.ret if self.ret else aa.typ)

class PyFunc(Func):
  def __init__(self, func):
    self.func = func
    lyli.object.Object.__init__(self, self, "func.PyFunc")
  def match(self, *args):
    return True
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
    lyli.object.Object.__init__(self, self, "func.PyFunc")
  def match(self, *_args):
    #print("TypedPyFunc.match : " + str(self) + ";" + str(_args))
    same_arity = (len(self.params_types) == len(_args))
    return same_arity and all([match_types(a,b) for (a, b) in zip(args_types(*_args), self.params_types)])
  def __call__(self, *_args):
    assert(len(self.params_types) == len(_args))
    args = [eval.eval_one(exp) for exp in _args]
    assert(self.match(*args))
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
    lyli.object.Object.__init__(self, self, "func.Macro")
  def match(self, *args):
    return True
  def __call__(self, *args):
    context.cur_ctx.update(zip(map(lambda x: str(x), self.params), args))
    ret = eval.eval_one(self.exp)
    return ret
    
class PyMacro(Macro):
  def __init__(self, func):
    self.func = func
    lyli.object.Object.__init__(self, self, "func.PyMacro")
  def match(self, *args):
    return True
  def __call__(self, *args):
    return self.func(*args)
  def __str__(self):
    ret = "[pymacro "
    ret += str(self.func)
    ret += "]"
    return ret

class TypedPyMacro(Macro):
  def __init__(self, params_types, func):
    self.func = func
    self.params_types = params_types
    assert(len(self.params_types) == func.__code__.co_argcount)
    lyli.object.Object.__init__(self, self, "func.PyMacro")
  def match(self, *_args):
    same_arity = (len(self.params_types) == len(_args))
    return same_arity and all([match_types(a,b) for (a, b) in zip(args_types(*_args), self.params_types)])
  def __call__(self, *args):
    assert(self.match(*args))
    return self.func(*args)
  def __str__(self):
    ret = "[pymacro "
    ret += str(self.func)
    ret += "]"
    return ret

class PolymorphicFunc(Func):
  def __init__(self, funcs):
    self.funcs = funcs
    lyli.object.Object.__init__(self, self, "func.PolymorphicFunc")
  def __call__(self, *_args):
    #print("PolymorphicFunc.__call__._args : " + str(_args))
    args = [eval.eval_one(exp) for exp in _args]
    #print("PolymorphicFunc.__call__.args : " + str(args))
    candidates = list(filter(lambda f: f.match(*args), self.funcs))
    if(len(candidates) == 1):
      return candidates[0].func(*args)
    else:
      print(args_types(*args))
      raise "TypeError"
  def __str__(self):
    ret = "[polyfn "
    for f in self.funcs:
      ret += str(f) + "\n"
    ret += "]"
    return ret

class PolymorphicMacro(Macro):
  def __init__(self, funcs):
    self.funcs = funcs
    lyli.object.Object.__init__(self, self, "func.PolymorphicFunc")
  def __call__(self, *args):
    candidates = list(filter(lambda f: f.match(*args), self.funcs))
    if(len(candidates) == 1):
      return candidates[0].func(*args)
    else:
      print(args_types(*args))
      print([str(x) for x in args])
      print(candidates)
      raise "TypeError"
  def __str__(self):
    ret = "[polyfn "
    for f in self.funcs:
      ret += str(f) + "\n"
    ret += "]"
    return ret

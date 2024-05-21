from .object import Object


class Func(Object):
  """
  Base class for all functions in Lyli.
  Functions are callable objects that has a list of instructions and parameters.
  They are exectued in the context of creation of the function.
  """
  pass


class Macro(Object):
  """
  Base class for all macros in Lyli.
  Macros are callable objects that has a list of instructions and parameters.
  They are exectued in the context of call to the macro.
  """
  pass


class BOp(Object):
  """
  Base class for all binary operators in Lyli.
  Binary operators are functions that takes two arguments and returns a value.
  """
  pass


class LyliFunc(Func):
  def __init__(self, params, exp, func_ctx):
    self.params = params
    self.exp = exp
    self.func_ctx = func_ctx

  def __repr__(self):
    return f"LyliFunc({self.params}, {self.exp})"


class PyBOp(BOp):

  def __init__(self, func):
    self.func = func

  def __repr__(self):
    return f"PyBOp({self.func})"


class PyFunc(Func):

  def __init__(self, func):
    self.func = func

  def __repr__(self):
    return f"PyFunc({self.func})"


class LyliMacro(Macro):

  def __init__(self, params, exp):
    self.params = params
    self.exp = exp

  def __repr__(self):
    return f"LyliMacro({self.params}, {self.exp})"


class PyMacro(Macro):

  def __init__(self, func):
    self.func = func

  def __repr__(self):
    return f"PyMacro({self.func})"

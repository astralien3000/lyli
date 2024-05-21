from lyli.ast import AST, Symbol, Atomic, List, Stmt, File
from lyli.context import Context
from lyli.object import Object, PyFunc


def call_PyFunc(pyfunc: PyFunc, args, ctx: Context):
  args = [eval(arg, ctx) for arg in args]
  return pyfunc.func(*args)


class ChainFunction:
  def __init__(self, final_func):
    self.func_list = []
    self.final_func = final_func
  
  def add(self, func):
    self.func_list.append(func)
    return func

  def __call__(self, ast: AST, ctx: Context):
    for func in self.func_list:
        ret = func(ast, ctx)
        if ret:
          return ret
    return self.final_func(ast, ctx)


@ChainFunction
def stmt(stmt : Stmt, ctx : Context) -> Object:
  raise TypeError(f"Unknown Stmt {stmt}")

@stmt.add
def stmt(stmt : Stmt, ctx : Context) -> Object:
  match stmt.args:
    case [Symbol(name), List(args)]:
      f = ctx[name]
      return call_PyFunc(f, args, ctx)
    case [expr]:
      return eval(expr, ctx)


def eval(ast : AST, ctx : Context) -> Object:
  if isinstance(ast, Symbol):
    return ctx[ast.name]
  elif isinstance(ast, Atomic):
    return ast.val
  elif isinstance(ast, List):
    return List([eval(arg, ctx) for arg in ast.args])
  elif isinstance(ast, File):
    ret = None
    for arg in ast.args:
      ret = eval(arg, ctx)
    return ret
  elif isinstance(ast, Stmt):
    return stmt(ast, ctx)
  else:
    raise TypeError(f"Unknown AST type: {type(ast)}")

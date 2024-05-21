from lyli import ast, context, object


def call_PyFunc(pyfunc: object.PyFunc, args, ctx: context.Context):
  args = [eval(arg, ctx) for arg in args]
  return pyfunc.func(*args)


class ChainFunction:
  def __init__(self, final_func):
    self.func_list = []
    self.final_func = final_func
  
  def add(self, func):
    self.func_list.append(func)
    return self

  def __call__(self, ast: ast.AST, ctx: context.Context):
    for func in self.func_list:
        ret = func(ast, ctx)
        if ret:
          return ret
    self.final_func(ast, ctx)


@ChainFunction
def stmt(stmt : ast.Stmt, ctx : context.Context) -> object.Object:
  raise TypeError(f"Unknown ast.Stmt {stmt}")

@stmt.add
def stmt(stmt : ast.Stmt, ctx : context.Context) -> object.Object:
  match stmt.args:
    case [ast.Symbol(name), ast.List(args)]:
      f = ctx[name]
      return call_PyFunc(f, args, ctx)
    case [expr]:
      return eval(expr, ctx)


def eval_ast(source : ast.AST, ctx : context.Context) -> object.Object:
  match source:
    case ast.Symbol():
      return ctx[source.name]
    case ast.Integer():
      return object.Integer(source.val)
    case ast.String():
      return object.String(source.val)
    case ast.Char():
      return object.Char(source.val)
    case ast.Float():
      return object.Float(source.val)
    case ast.List():
      return object.List([eval(arg, ctx) for arg in source.args])
    case ast.File():
      ret = None
      for arg in source.args:
        ret = eval(arg, ctx)
      return ret
    case ast.Stmt():
      return stmt(source, ctx)
    case _:
      raise TypeError(f"Unknown AST type: {type(source)}")


def eval(source, ctx : context.Context) -> object.Object:
  if isinstance(source, str):
    source = ast.parse(source)
  return eval_ast(source, ctx)

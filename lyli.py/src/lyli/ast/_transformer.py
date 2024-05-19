import lark

import lyli.ast._ast as _ast


class Transformer(lark.Transformer):

  def file(self, args):
    return _ast.File(args[0])

  def expr(self, args):
    return args[0]

  def stmt(self, args):
    return _ast.Stmt(args)

  def atomic_expr(self, args):
    return args[0]

  def list_expr(self, args):
    return _ast.List(*args)

  def stmt_list(self, args):
    return args

  def string_expr(self, args):
    return _ast.String(str(args[0])[1:-1])

  def longstring_expr(self, args):
    return _ast.String(str(args[0])[3:-3])

  def char_expr(self, args):
    return _ast.Char(str(args[0])[1:-1])

  def integer_expr(self, args):
    return _ast.Integer(str(args[0]))

  def float_expr(self, args):
    return _ast.Float(str(args[0]))
  
  def symbol_expr(self, args):
    return _ast.Symbol(str(args[0]))

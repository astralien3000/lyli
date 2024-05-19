import lark

import lyli.ast._ast as _ast


class Transformer(lark.Transformer):

  def file(self, args):
    return _ast.File(args[0])

  def expr(self, args):
    return args[0]

  def stmt(self, args):
    return _ast.Stmt(args)

  def atomic(self, args):
    return args[0]

  def list(self, args):
    return _ast.List(*args)

  def stmt_list(self, args):
    return args

  def string(self, args):
    return _ast.String(str(args[0])[1:-1])

  def longstring(self, args):
    return _ast.String(str(args[0])[3:-3])

  def char(self, args):
    return _ast.Char(str(args[0])[1:-1])

  def integer(self, args):
    return _ast.Integer(str(args[0]))

  def float(self, args):
    return _ast.Float(str(args[0]))
  
  def symbol(self, args):
    return _ast.Symbol(str(args[0]))

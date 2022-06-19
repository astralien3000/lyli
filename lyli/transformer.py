import lark

import lyli.ast as ast


class Transformer(lark.Transformer):

  def file(self, args):
    return ast.Call([ast.Symbol("file"), *args[0]])

  def instr(self, args):
    return args[0]

  def expr(self, args):
    return args[0]

  def stmt(self, *args):
    return ast.Call([ast.Symbol("stmt"), *args[0]])

  def atomic_expr(self, args):
    return args[0]

  def call_expr(self, args):
    return ast.Call([args[0], *args[1]])

  def instr_list(self, args):
    return args

  def string_expr(self, args):
    return ast.String(str(args[0])[1:-1])

  def longstring_expr(self, args):
    return ast.String(str(args[0])[3:-3])

  def char_expr(self, args):
    return ast.Char(str(args[0])[1:-1])

  def integer_expr(self, args):
    return ast.Integer(str(args[0]))

  def float_expr(self, args):
    return ast.Float(str(args[0]))
  
  def symbol_expr(self, args):
    return ast.Symbol(str(args[0]))

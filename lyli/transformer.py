import lark

import lyli.ast as ast


def associate(args):
  if len(args) > 3:
    return ast.Call([
      args[1], args[0], associate(args[2:])
    ])
  elif len(args) == 3:
    return ast.Call([
      args[1], args[0], args[2]
    ])
  else:
    return ast.Call([
      args[1], args[0], ast.Symbol("_")
    ])


class Transformer(lark.Transformer):
  def instr(self, args):
    return args[0]
  def expr(self, args):
    return args[0]
  def call_expr(self, args):
      #print("CALL_EXPR " + str(args))
    return ast.Call([args[0], *args[1]])
  def atomic_expr(self, args):
    return args[0]
  def par_expr(self, args):
    return args[0]
  def bop_expr(self, args):
    return associate(args)
  def bop_stmt(self, args):
    return associate(args)

  def uop_stmt(self, args):
    return ast.Call([args[0], args[1]])

  def start(self, args):
    return ast.Call([ast.Symbol("$"), *args[0]])

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

  def operator(self, args):
    return ast.Symbol(str(args[0]))

  def stmt(self, *args):
      #print("STMT " + str(*args))
    return ast.Call([ast.Symbol("_"), args[0][0]] + args[0][1:])
    
  def instr_list(self, args):
    return args

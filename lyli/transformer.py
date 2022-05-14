import lark

import lyli.ast as ast

class Transformer(lark.Transformer):
  def instr(self, args):
    return args[0]
  def expr(self, args):
    return args[0]
  def uop_expr(self, args):
    return args[0]
  def call_expr(self, args):
      #print("CALL_EXPR " + str(args))
    return ast.Call([args[0]] + args[1])
  def atomic_expr(self, args):
    return args[0]
  def par_expr(self, args):
    return args[0]
  def bop_expr(self, args):
    while len(args) > 1:
      args = [
        ast.Call([args[1], args[0], args[2]]),
        *args[3:],
      ]
    print("LOOL ", args[0])
    return args[0]
  def bop_stmt(self, args):
    while len(args) > 1:
      args = [
        ast.Call([args[1], args[0], args[2]]),
        *args[3:],
      ]
    print("LOOL STMT ", args[0])
    return args[0]

  def uop_prefix_expr(self, args):
    return ast.Call([ast.Call([ast.Symbol("pre"), args[0]]), args[1]])
  def uop_suffix_expr(self, args):
    return ast.Call([ast.Call([ast.Symbol("post"), args[1]]), args[0]])

  def start(self, args):
    return ast.Call([ast.Symbol("$")] + args[0])

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
      #print(args[0])
    return ast.Symbol(args[0])

  def cmpd_bop(self, args):
    return ast.Symbol(args[0])
  def smpl_bop(self, args):
    return ast.Symbol(args[0])
  def suf_uop(self, args):
    return ast.Symbol(args[0])
  def buop(self, args):
    return ast.Symbol(args[0])
  def puop(self, args):
    return ast.Symbol(args[0])
  def par_bop(self, args):
    return ast.Symbol(args[0])
  def pre_uop(self, args):
    return args[0]
  def all_bop(self, args):
    return args[0]
  def buop(self, args):
    return args[0]
  def operator(self, args):
    return args[0]

  def stmt(self, *args):
      #print("STMT " + str(*args))
    return ast.Call([ast.Symbol("_"), args[0][0]] + args[0][1:])
    
  def instr_list(self, args):
    return args

from ._ast import *


def unparse(ast: AST):
  return globals()["unparse_" + ast.__class__.__name__](ast)

def unparse_AST(ast: AST):
  raise NotImplementedError()

def unparse_Expr(expr: Expr):
  raise NotImplementedError()

def unparse_Atomic(expr: Atomic):
  raise NotImplementedError()

def unparse_Symbol(expr: Symbol):
  return expr.val

def unparse_String(expr: String):
  return f'"{expr.val}"'

def unparse_Char(expr: Char):
  return f"'{expr.val}'"

def unparse_Integer(expr: Integer):
  return str(expr.val)

def unparse_Float(expr: Float):
  return str(expr.val)

def unparse_List(expr: List):
  return f"({', '.join([unparse(e) for e in expr])})"

def unparse_Stmt(stmt: Stmt):
  return " ".join([unparse(e) for e in stmt])

def unparse_File(file: File):
  return ";\n".join([unparse(e) for e in file])

from ._ast import *


def unparse(ast: AST):
  return globals()["unparse_" + ast.__class__.__name__](ast)

def unparse_AST(ast: AST):
  raise TypeError(f"unparse_AST not implemented for {ast.__class__.__name__}")

def unparse_Expr(ast: Expr):
  raise TypeError(f"unparse_AST not implemented for {ast.__class__.__name__}")

def unparse_Atomic(ast: Atomic):
  raise TypeError(f"unparse_AST not implemented for {ast.__class__.__name__}")

def unparse_Symbol(ast: Symbol):
  return ast.val

def unparse_String(ast: String):
  return f'"{ast.val}"'

def unparse_Char(ast: Char):
  return f"'{ast.val}'"

def unparse_Integer(ast: Integer):
  return str(ast.val)

def unparse_Float(ast: Float):
  return str(ast.val)

def unparse_List(ast: List):
  return f"({', '.join([unparse(e) for e in ast])})"

def unparse_Stmt(stmt: Stmt):
  return " ".join([unparse(e) for e in stmt])

def unparse_File(file: File):
  return ";\n".join([unparse(e) for e in file])

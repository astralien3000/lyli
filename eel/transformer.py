import lark

from .instr import *

class EelTransformer(lark.Transformer):
    def instr(self, args):
        return args[0]
    def expr(self, args):
        return args[0]
    def call_expr(self, args):
        return args[0]
    def atomic_expr(self, args):
        return args[0]

    def start(self, *args):
        return Global(*args)

    def integer_expr(self, args):
        return int(args[0])
    def string_expr(self, args):
        return str(args[0])
    def symbol_expr(self, args):
        return Symbol(args[0])

    def operator(self, args):
        return args[0]

    def paren_call_expr(self, *args):
        return PCall(*args)
    def brace_call_expr(self, *args):
        return BCall(*args)
    def stmt(self, *args):
        return BCall([PCall([Symbol("_"), args[0][0]])] + args[0][1:])

    def not_(self, _):
        return Symbol("!")
    def bwnot(self, _):
        return Symbol("~")

    def mul(self, _):
        return Symbol("*")

    def div(self, _):
        return Symbol("/")
    def mod(self, _):
        return Symbol("%")

    def add(self, _):
        return Symbol("+")
    def sub(self, _):
        return Symbol("-")

    def lt(self, _):
        return Symbol("<")
    def gt(self, _):
        return Symbol(">")
    def le(self, _):
        return Symbol("<=")
    def ge(self, _):
        return Symbol(">=")

    def eq(self, _):
        return Symbol("==")
    def neq(self, _):
        return Symbol("!=")

    def or_(self, _):
        return Symbol("||")

    def dot(self, _):
        return Symbol(".")
    def arrow(self, _):
        return Symbol("->")

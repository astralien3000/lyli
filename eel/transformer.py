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
        print(args[0])
        return Symbol(args[0])

    def operator(self, args):
        return Symbol(args[0])

    def paren_call_expr(self, *args):
        return PCall(*args)
    def brace_call_expr(self, *args):
        return BCall(*args)
    def stmt(self, *args):
        return BCall([PCall([Symbol("_"), args[0][0]])] + args[0][1:])

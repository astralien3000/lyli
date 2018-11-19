import lark

from eel_instr import *

class EelTransformer(lark.Transformer):
    def precedence_0_expr(self, (arg,)):
        return arg
    def precedence_1_expr(self, (arg,)):
        return arg
    def precedence_2_expr(self, (arg,)):
        return arg
    def precedence_3_expr(self, (arg,)):
        return arg
    def precedence_5_expr(self, (arg,)):
        return arg
    def precedence_6_expr(self, (arg,)):
        return arg
    def precedence_9_expr(self, (arg,)):
        return arg
    def precedence_10_expr(self, (arg,)):
        return arg
    def precedence_15_expr(self, (arg,)):
        return arg
    def precedence_16_expr(self, (arg,)):
        return arg

    def instr(self, (arg,)):
        return arg
    def expr(self, (arg,)):
        return arg
    def call_expr(self, (arg,)):
        return arg
    def atomic_expr(self, (arg,)):
        return arg

    def start(self, *args):
        return Global(*args)

    def integer_expr(self, (arg,)):
        return int(arg)
    def string_expr(self, (arg,)):
        return str(arg)
    def symbol_expr(self, (arg,)):
        return Symbol(arg)

    def operator(self, (arg,)):
        return arg

    def paren_call_expr(self, *args):
        return PCall(*args)
    def brace_call_expr(self, *args):
        return BCall(*args)
    def stmt(self, *args):
        return BCall([PCall([Symbol("_"), args[0][0]])] + args[0][1:])

    def unary_expr(self, (op, right)):
        return PCall([op, right])
    def not_(self, _):
        return Symbol("!")
    def bwnot(self, _):
        return Symbol("~")

    def mul(self, _):
        return Symbol("*")

    def mul_expr(self, (left, op, right)):
        return PCall([op, left, right])
    def div(self, _):
        return Symbol("/")
    def mod(self, _):
        return Symbol("%")

    def add_sub_expr(self, (left, op, right)):
        return PCall([op, left, right])
    def add(self, _):
        return Symbol("+")
    def sub(self, _):
        return Symbol("-")

    def cmp_expr(self, (left, op, right)):
        return PCall([op, left, right])
    def lt(self, _):
        return Symbol("<")
    def gt(self, _):
        return Symbol(">")
    def le(self, _):
        return Symbol("<=")
    def ge(self, _):
        return Symbol(">=")

    def eq_expr(self, (left, op, right)):
        return PCall([op, left, right])
    def eq(self, _):
        return Symbol("==")
    def neq(self, _):
        return Symbol("!=")

    def or_expr(self, (left, op, right)):
        return PCall([op, left, right])
    def or_(self, _):
        return Symbol("||")

    def assign_expr(self, (left, right)):
        return PCall([Symbol("="), left, right])

    def dot_expr(self, (left, dot, right)):
        return BCall([PCall([Symbol(dot), left]), right])
    def dot(self, _):
        return Symbol(".")
    def arrow(self, _):
        return Symbol("->")

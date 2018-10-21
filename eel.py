#!/usr/bin/python
# coding: UTF-8

import lark

class Symbol(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

class PCall(list):
    def __str__(self):
        ret = str(self[0])
        ret += "("
        for a in self[1:]:
            ret += str(a)
            ret += ","
        ret += ")"
        return ret

class BCall(list):
    def __str__(self):
        ret = str(self[0])
        ret += "{"
        for a in self[1:]:
            ret += str(a)
            ret += ";"
        ret += "}"
        return ret

class Global(list):
    def __str__(self):
        ret = ""
        for a in self:
            ret += str(a)
            ret += ";\n"
        return ret

class EelTransformer(lark.Transformer):
    def precedence_0_expr(self, (arg,)):
        return arg
    def precedence_1_expr(self, (arg,)):
        return arg
    def precedence_2_expr(self, (arg,)):
        return arg
    def precedence_6_expr(self, (arg,)):
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

    def paren_call_expr(self, *args):
        return PCall(*args)
    def brace_call_expr(self, *args):
        return BCall(*args)
    def stmt(self, *args):
        return BCall(*args)

    def add_sub_expr(self, (left, op, right)):
        return PCall([op, left, right])
    def add(self, _):
        return Symbol("+")
    def sub(self, _):
        return Symbol("-")

    def assign_expr(self, (left, right)):
        return PCall([Symbol("="), left, right])

eel_parser = lark.Lark.open("eel.lark", parser="lalr", transformer=EelTransformer())

with open("examples/test.eel", "r") as f:
    ast = eel_parser.parse(f.read())
    print ast

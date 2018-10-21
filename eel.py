#!/usr/bin/python
# coding: UTF-8

import lark

class Symbol(str):
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

class Context(dict):
    def __init__(self, pairs={}, parent=None):
        dict.__init__(self, pairs)
        self.parent = parent
    def search(self, key):
        if key in self:
            return self
        elif self.parent:
            return self.parent.search(key)
        else:
            return None
    def __getitem__(self, key):
        ctx = self.search(key)
        if ctx:
            return dict.__getitem__(ctx, key)
        else:
            return None
    def __setitem__(self, key, val):
        ctx = self.search(key)
        if ctx:
            dict.__setitem__(ctx, key, val)

cur_ctx = Context()

def global_context(self):
    global cur_ctx
    def _print(args):
        print(args)
    def _def(*args):
        if isinstance(args[-1], list) and args[-1][0] == "=":
            cur_ctx.update({args[-1][1] : args[-1][2]})
        else:
            raise "ERROR"
    ret = Context({
        "print" : _print,
        "def" : _def,
    }, self)
    import operator as op
    ret.update({
        "+" : op.add,
        "-" : op.sub,
    })
    return ret

cur_ctx = global_context(cur_ctx)

def eval(x):
    if isinstance(x, Symbol):
        return cur_ctx[x]
    elif not isinstance(x, list):
        return x
    else:
        proc = eval(x[0])
        if isinstance(x, BCall):
            args = x[1:]
            return proc(*args)
        else:
            args = [eval(exp) for exp in x[1:]]
            return proc(*args)

with open("examples/test.eel", "r") as f:
    ast = eel_parser.parse(f.read())
    print ast
    for e in ast:
        res = eval(e)
        if res: print res

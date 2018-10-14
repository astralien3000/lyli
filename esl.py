#!/usr/bin/python
# coding: UTF-8

"""
Even Simpler Lisp (ESL) Interpreter

Copyright (C) 2018 Loïc Dauphin <astralien3000@yahoo.fr>

Based on the work :
Copyright (C) 2010 Peter Norvig, see http://norvig.com/lispy2.html

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

################ Symbol, Func, classes

import re
import sys
import StringIO
import random

class Symbol(str): pass

_quote = Symbol("quote")
_quasiquote = Symbol("quasiquote")
_unquote = Symbol("unquote")
_unquotesplicing = Symbol("unquote-splicing")

class Func(object):
    "A user-defined procedure."
    def __init__(self, params, exp, env):
        self.params, self.exp, self.env = params, exp, env
    def __call__(self, *args):
        global cur_env
        prev_env = cur_env
        cur_env =  Env(self.params, args, self.env)
        ret = eval(self.exp)
        cur_env = prev_env
        return ret

class Macro(object):
    "A user-defined macro."
    def __init__(self, params, exp):
        self.params, self.exp = params, exp
    def __call__(self, *args):
        global cur_env
        cur_env = Env((), (), Env(self.params, args, cur_env))
        ret = eval(eval(self.exp))
        macro_env = cur_env
        cur_env = cur_env.outer.outer
        cur_env.update(macro_env)
        return ret

class NativeMacro(Macro):
    "A callable object"
    def __init__(self, func):
        self.func = func
    def __call__(self, *args):
        return self.func(*args)

################ parse, read, and user interaction

def parse(inport):
    "Parse a program: read and expand/error-check it."
    # Backwards compatibility: given a str, convert it to an InPort
    if isinstance(inport, str): inport = InPort(StringIO.StringIO(inport))
    return read(inport)

eof_object = Symbol('#<eof-object>') # Note: uninterned; can't be read

class InPort(object):
    "An input port. Retains a line of chars."
    tokenizer = r"""\s*(,@|[('`,)]|"(?:[\\].|[^\\"])*"|;.*|[^\s('"`,;)]*)(.*)"""
    def __init__(self, file):
        self.file = file; self.line = ''
    def next_token(self):
        "Return the next token, reading new text into line buffer if needed."
        while True:
            if self.line == '': self.line = self.file.readline()
            if self.line == '': return eof_object
            token, self.line = re.match(InPort.tokenizer, self.line).groups()
            if token != '' and not token.startswith(';'):
                return token

def readchar(inport):
    "Read the next character from an input port."
    if inport.line != '':
        ch, inport.line = inport.line[0], inport.line[1:]
        return ch
    else:
        return inport.file.read(1) or eof_object

def read(inport):
    "Read a Scheme expression from an input port."
    def read_ahead(token):
        if '(' == token: 
            L = []
            while True:
                token = inport.next_token()
                if token == ')': return L
                else: L.append(read_ahead(token))
        elif ')' == token: raise SyntaxError('unexpected )')
        elif token in quotes: return [quotes[token], read(inport)]
        elif token is eof_object: raise SyntaxError('unexpected EOF in list')
        else: return atom(token)
    # body of read:
    token1 = inport.next_token()
    return eof_object if token1 is eof_object else read_ahead(token1)

quotes = {"'":_quote, "`":_quasiquote, ",":_unquote, ",@":_unquotesplicing}

def atom(token):
    'Numbers become numbers; #t and #f are booleans; "..." string; otherwise Symbol.'
    if token == '#t': return True
    elif token == '#f': return False
    elif token[0] == '"': return token[1:-1].decode('string_escape')
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            try: return complex(token.replace('i', 'j', 1))
            except ValueError:
                return Symbol(token)

def to_string(x):
    "Convert a Python object back into a Lisp-readable string."
    if x is True: return "#t"
    elif x is False: return "#f"
    elif isinstance(x, Symbol): return x
    elif isinstance(x, str): return '"%s"' % x.encode('string_escape').replace('"',r'\"')
    elif isinstance(x, list): return '('+' '.join(map(to_string, x))+')'
    elif isinstance(x, complex): return str(x).replace('j', 'i')
    else: return str(x)

def load(filename):
    "Eval every expression from a file."
    repl(None, InPort(open(filename)), None)

def repl(prompt='lispy> ', inport=InPort(sys.stdin), out=sys.stdout):
    "A prompt-read-eval-print loop."
    sys.stderr.write("Lispy version 2.0\n")
    while True:
        try:
            if prompt: sys.stderr.write(prompt)
            x = parse(inport)
            if x is eof_object: return
            val = eval(x)
            if val is not None and out: print >> out, to_string(val)
        except Exception as e:
            print '%s: %s' % (type(e).__name__, e)

################ Environment class

class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, params=(), args=(), outer=None):
        # Bind parm list to corresponding args, or single parm to list of args
        self.outer = outer
        if isinstance(params, Symbol): 
            self.update({params:list(args)})
        else: 
            if len(args) != len(params):
                raise TypeError('expected %s, given %s, ' 
                                % (to_string(params), to_string(args)))
            self.update(zip(params,args))
    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self: return self
        elif self.outer is None: raise LookupError(var)
        else: return self.outer.find(var)

cur_env = Env()

def is_pair(x): return x != [] and isinstance(x, list)
def cons(x, y): return [x]+y

def callcc(proc):
    "Call proc with current continuation; escape only"
    ball = RuntimeWarning("Sorry, can't continue this continuation any longer.")
    def throw(retval): ball.retval = retval; raise ball
    try:
        return proc(throw)
    except RuntimeWarning as w:
        if w is ball: return ball.retval
        else: raise w

def macro_set(sym, val):
    cur_env.find(sym)[sym] = eval(val)
    return None

def macro_define(sym, val):
    cur_env[sym] = eval(val)
    return None

def macro_lambda(args, exp):
    return Func(args, exp, cur_env)

def macro_macro(args, exp):
    return Macro(args, exp)

def macro_if(cond, then_exp, else_exp):
    return eval(then_exp if eval(cond) else else_exp)

def macro_begin(*args):
    args = list(args)
    for exp in args:
        eval(exp)
    return args[-1]

def macro_quote(arg):
    return arg

def macro_quasiquote(exp):
    if not isinstance(exp, list):
        return exp
    else:
        ret = []
        for e in exp:
            if not isinstance(e, list):
                ret.append(e)
            elif e[0] == _unquote:
                ret.append(eval(e[1]))
            elif e[0] == _unquotesplicing:
                ret += eval(e[1])
            else:
                ret.append(macro_quasiquote(e))
        return ret

def add_globals(self):
    "Add some standard procedures."
    import math, cmath, operator as op
    self.update({
        'fn': NativeMacro(macro_lambda),
        'macro': NativeMacro(macro_macro),

        _quote: NativeMacro(macro_quote),

        _quasiquote: NativeMacro(macro_quasiquote),

        'set': NativeMacro(macro_set),
        'def': NativeMacro(macro_define),
        'if': NativeMacro(macro_if),
        'begin': NativeMacro(macro_begin),
    })
    self.update(vars(math))
    self.update(vars(cmath))
    self.update({
        '+':op.add,
        '-':op.sub,
        '*':op.mul,
        '/':op.div,
        'not':op.not_, 
        '>':op.gt,
        '<':op.lt,
        '>=':op.ge,
        '<=':op.le,
        '=':op.eq, 
        'equal?':op.eq,
        'eq?':op.is_,
        'length':len,
        'cons':cons,
        'car':lambda x:x[0],
        'cdr':lambda x:x[1:],
        'append':op.add,  
        'list':lambda *x:list(x),
        'list?': lambda x:isinstance(x,list),
        'null?':lambda x:x==[],
        'symbol?':lambda x: isinstance(x, Symbol),
        'boolean?':lambda x: isinstance(x, bool),
        'pair?':is_pair, 
        'apply':lambda proc,l: proc(*l),
        'eval':lambda x: eval(expand(x)),
        'print':lambda x,port=sys.stdout:port.write(x if isinstance(x,str) else to_string(x)),
        'rand': lambda val: int(random.random() * val),
    })
    return self

cur_env = add_globals(cur_env)

################ eval

def eval(x):
    global cur_env
    if isinstance(x, Symbol):
        return cur_env.find(x)[x]
    elif not isinstance(x, list):
        return x
    elif len(x) == 0:
        return None
    else:
        proc = eval(x[0])
        if isinstance(proc, Macro):
            args = x[1:]
            return proc(*args)
        else:
            args = [eval(exp) for exp in x[1:]]
            return proc(*args)

################ main

if __name__ == '__main__':
    tests = [
        "(((fn (a) (fn (b) (+ a b))) 2) 40)",

        "(def a (macro (x) (list? x)))",
        "(a 5)",
        "(a (+ 5 5))",
        "(a '(+ 5 5))",

        "(def b (fn (x) (list? x)))",
        "(b 5)",
        "(b (+ 5 5))",
        "(b '(+ 5 5))",

        "(def test (fn (x) (def miew x)))",
        "(test 42)",
        "'miew",

        "(def test (macro (x) (def miew x)))",
        "(test 42)",
        "miew",

        "(def miew (fn () (print \"miew!\")))",
        "(miew)",

        "(def mif (fn (cnd) (if cnd (macro (a b) a) (macro (a b) b))))",
        "((mif #t) (print 1) (print 2))",
        "((mif #f) (print 1) (print 2))",

        "(def n '(42 666))",
        "(list 'n n)",
        "`(n ,n)",
        "`(n ,@n)",
    ]
    for test in tests:
        print("> " + test)
        print parse(test)
        #print esl_parser.parse(test)
        print EslTransformer().transform(esl_parser.parse(test))
        res = eval(parse(test))
        if res: print res
    repl()

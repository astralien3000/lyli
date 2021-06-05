#!/usr/bin/python3
# coding: UTF-8

import lark

from eel.instr import *
from eel.transformer import *
from eel.context import *
from eel.func import *
from eel.eval import *
import eel

eel.parser = lark.Lark(open("eel.lark", "r", encoding="utf-8"), parser="lalr", transformer=EelTransformer())

def global_context(self):
    def _print(args):
        print(args)
    def _defint(*args):
        if isinstance(args[0], list) and str(args[0][0]) == '=':
            eel.context.cur_ctx.update({str(args[0][1]) : args[0][2]})
        elif len(args) == 1:
            eel.context.cur_ctx.update({str(args[0]) : 0})
        else:
            raise Exception("WRONG DEFINE FORM")
        return None
    def _defvar(*args):
        if isinstance(args[0], list) and args[0][0] == '=':
            eel.context.cur_ctx.update({str(args[0][1]) : args[0][2]})
        elif len(args) == 1:
            eel.context.cur_ctx.update({str(args[0]) : 0})
        else:
            raise Exception("WRONG DEFINE FORM")
        return None
    def _fn(*args):
        if isinstance(args[-1], list):
            params = list(map(lambda x: x[2], args[-1][0][1:]))
            params_types = list(map(lambda x: x[1], args[-1][0][1:]))
            eel.context.cur_ctx.update({
                str(args[-1][0][0]) : Func(args[-1][0][0], args[-2], params_types, params, args[-1][1:], eel.context.cur_ctx)
            })
        else:
            raise Exception("WRONG DEFINE FORM")
    def _macro(*args):
        if isinstance(args[0], list):
            sym = args[0][0][0]
            params = args[0][0][1:]
            exp = args[0][1:]
            #print("sym : " + str(sym))
            #print("params : " + str(params))
            #print("exp : " + str(exp))
            eel.context.cur_ctx.update({
                str(sym) : Macro(sym, params, exp)
            })
        else:
            raise Exception("WRONG DEFINE FORM")
    def _if(arg):
        if arg:
            return lambda a: eval(a)
        return lambda a: None
    def _ret(*args):
        if len(args) == 1:
            return Func.Return(eval(args[0]))
        else:
            return Func.Return(eval(BCall([Symbol("_"), *args])))
    def _import(arg):
        import importlib
        mod = importlib.import_module(str(arg))
        eel.context.cur_ctx.update(vars(mod))
        return None
    def _(*args):
      opexpr = [*args]
      #print("OP EXPR ? " + str(opexpr))
      for op in ["::",".","*","/","+","-","<","==","="]:
        found = True
        while found:
          found = False
          for i in range(0, len(opexpr)):
            before = []
            after = []
            if i + 2 < len(opexpr):
              after = opexpr[i+2:]
            if i - 1 > 0:
              before = opexpr[:i-1]
            if str(opexpr[i]) == op:
              opexpr = before + [Call([opexpr[i], opexpr[i-1], opexpr[i+1]])] + after
              found = True
              #print(opexpr)
              break
      if(callable(eval(opexpr[0]))):
        return eval(Call(opexpr))
      return eval(opexpr[0])
    def _defstruct(*args):
        import ctypes
        name = str(args[0][0])
        members = args[0][1:]
        fields = []
        for m in members:
            if(str(m[1]) == "int"):
                fields.append((str(m[2]), ctypes.c_int))
        
        eel.context.cur_ctx.update({
            "LOL::" + name : Context()
        })
        class DefStruct(ctypes.Structure):
            _fields_ = fields
        def _def(*args):
            if len(args) == 1:
                eel.context.cur_ctx.update({
                    str(args[0]) : DefStruct(),
                    str(args[0]) + "::type" : Symbol(name),
                })
                eel.context.cur_ctx.update({
                    "LOL::" + str(args[0]) : Context()
                })
                eel.context.cur_ctx["LOL::" + str(args[0])].update({
                    "value" : DefStruct(),
                    "type" : Symbol(name),
                })
                #print(eel.context.cur_ctx)
            else:
                raise Exception("WRONG DEFINE FORM" + str([*args]))
            return None
        eel.context.cur_ctx.update({
            name : PyMacro(_def)
        })
        eel.context.cur_ctx["LOL::" + name].update({
            "def" : PyMacro(_def)
        })
        def _get(memb):
            return lambda *args: getattr(args[0], memb)
        def _set(memb):
            return lambda *args: setattr(args[0], memb, args[1])
        for m in members:
            eel.context.cur_ctx.update({
                name + "::get_" + str(m[2]) : _get(str(m[2])),
                name + "::set_" + str(m[2]) : _set(str(m[2])),
            })
            eel.context.cur_ctx["LOL::" + name].update({
                "get_" + str(m[2]) : _get(str(m[2])),
                "set_" + str(m[2]) : _set(str(m[2])),
            })
        #print(eel.context.cur_ctx)
    def _scope(arg1, arg2):
      if isinstance(arg2, Call):
        return Call([eel.context.cur_ctx["LOL::"+arg1][arg2[0]]] + arg2[1:])
      return eval(eel.context.cur_ctx["LOL::"+ str(arg1)][str(arg2)])
    def _dot(arg1, arg2):
      arg1_type = eel.context.cur_ctx["LOL::"+ str(arg1)]["type"]
      if isinstance(arg2, Call):
        return eval(Call([_scope(arg1_type, arg2[0]), arg1] + arg2[1:]))
      return eval(Call([_scope(arg1_type, arg2), arg1]))
    def _block(*args):
      prev_ctx = eel.context.cur_ctx
      eel.context.cur_ctx =  Context({}, prev_ctx)
      for a in args:
        eval(a)
      eel.context.cur_ctx = prev_ctx
      return None
    def _set(arg1, arg2):
      eel.context.cur_ctx[str(arg1)] = eval(arg2)
    ret = Context({
        "_" : PyMacro(_),
        "print" : PyFunc("print", _print),
        "int" : PyMacro(_defint),
        "var" : PyMacro(_defvar),
        "fn" : PyMacro(_fn),
        "macro" : PyMacro(_macro),
        "if" : PyFunc("if", _if),
        "return" : PyMacro(_ret),
        "import" : PyMacro(_import),
        "struct" : PyMacro(_defstruct),
        "$" : PyFunc("eval", eval),
        "block" : PyMacro(_block),
        "::" : PyMacro(_scope),
        "." : PyMacro(_dot),
        "=" : PyMacro(_set),
    }, self)
    import operator as op
    ret.update({
        "+" : BOp("+", op.add),
        "-" : BOp("-", op.sub),
        "*" : BOp("*", op.mul),
        "!" : BOp("!", op.not_),
        "~" : BOp("~", op.inv),
        "<" : BOp("<", op.lt),
        ">" : BOp(">", op.gt),
        "<=" : BOp("<=", op.le),
        ">=" : BOp(">=", op.ge),
        "==" : BOp("==", op.eq),
        "!=" : BOp("!=", op.ne),
        "||" : BOp("||", op.or_),
    })
    return ret

eel.context.cur_ctx = global_context(eel.context.cur_ctx)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            ast = eel.parser.parse(f.read())
            print("---------------- AST BEG ----------------")
            print(ast)
            print("---------------- AST END ----------------")
            res = eval(ast)
            if res: print(res)
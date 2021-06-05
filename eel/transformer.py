import lark

from .instr import *

class EelTransformer(lark.Transformer):
    def instr(self, args):
        return args[0]
    def expr(self, args):
        return args[0]
    def call_expr(self, args):
        #print("CALL_EXPR " + str(args))
        return PCall([args[0]] + args[1])
    def atomic_expr(self, args):
        return args[0]

    def start(self, args):
        return Global(args[0])

    def string_expr(self, args):
        return String(str(args[0])[1:-1])
    def longstring_expr(self, args):
        return String(str(args[0])[2:-2])
    
    def integer_expr(self, args):
        return int(args[0])
    
    def symbol_expr(self, args):
        #print(args[0])
        return Symbol(args[0])

    def operator_expr(self, args):
        #print(args)
        return Symbol(args[0])
    
    def operator(self, args):
        return Symbol(args[0])

    def stmt(self, *args):
        #print("STMT " + str(*args))
        return PCall([Symbol("_"), args[0][0]] + args[0][1:])
      
    def instr_list(self, args):
        return args

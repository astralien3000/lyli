import lark

import lyli.expr_tree as expr_tree

class Transformer(lark.Transformer):
    def instr(self, args):
        return args[0]
    def expr(self, args):
        return args[0]
    def call_expr(self, args):
        #print("CALL_EXPR " + str(args))
        return expr_tree.Call([args[0]] + args[1])
    def atomic_expr(self, args):
        return args[0]

    def start(self, args):
        return expr_tree.Call([expr_tree.Symbol("$")] + args[0])

    def string_expr(self, args):
        return expr_tree.String(str(args[0])[1:-1])
    def longstring_expr(self, args):
        return expr_tree.String(str(args[0])[2:-2])
    
    def integer_expr(self, args):
        return expr_tree.Integer(int(args[0]))
    
    def symbol_expr(self, args):
        #print(args[0])
        return expr_tree.Symbol(args[0])

    def operator(self, args):
        return expr_tree.Symbol(args[0])

    def stmt(self, *args):
        #print("STMT " + str(*args))
        return expr_tree.Call([expr_tree.Symbol("_"), args[0][0]] + args[0][1:])
      
    def instr_list(self, args):
        return args

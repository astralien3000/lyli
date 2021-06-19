import lyli.context as context
import lyli.ast as ast
import lyli.func as func
import lyli.eval as eval

import operator

def _print(args):
    print(args)

def _defint(*args):
    if isinstance(args[0], ast.Call) and str(args[0][0]) == '=':
        context.cur_ctx.update({str(args[0][1]) : args[0][2]})
    elif len(args) == 1:
        context.cur_ctx.update({str(args[0]) : 0})
    else:
        raise Exception("WRONG DEFINE FORM")
    return None

def _defvar(*args):
    if isinstance(args[0], ast.Call) and args[0][0] == '=':
        context.cur_ctx.update({str(args[0][1]) : args[0][2]})
    elif len(args) == 1:
        context.cur_ctx.update({str(args[0]) : 0})
    else:
        raise Exception("WRONG DEFINE FORM")
    return None

def _fn(*args):
    if len(args) == 2 and isinstance(args[-1], ast.Call):
        params = list(map(lambda x: x[2], args[-1][0][1:]))
        params_types = list(map(lambda x: x[1], args[-1][0][1:]))
        context.cur_ctx.update({
            str(args[-1][0][0]) : func.Func(args[-2], params_types, params, args[-1][1:], context.cur_ctx)
        })
    elif len(args) == 1 and isinstance(args[-1], ast.Call):
        params = list(map(lambda x: x[2], args[-1][0][1:]))
        params_types = list(map(lambda x: x[1], args[-1][0][1:]))
        context.cur_ctx.update({
            str(args[-1][0][0]) : func.Func(None, params_types, params, args[-1][1:], context.cur_ctx)
        })
    else:
        raise Exception("WRONG DEFINE FORM")

def _macro(*args):
    if isinstance(args[0], ast.Call):
        sym = args[0][0][0]
        params = args[0][0][1:]
        exp = args[0][1:]
        #print("sym : " + str(sym))
        #print("params : " + str(params))
        #print("exp : " + str(exp))
        context.cur_ctx.update({
            str(sym) : func.Macro(params, exp)
        })
    else:
        raise Exception("WRONG DEFINE FORM")

def _if(arg):
    if arg:
        return func.PyFunc(lambda a: eval.eval_one(a))
    return func.PyFunc(lambda a: None)

def _ret(*args):
    if len(args) == 1:
        return func.Func.Return(eval.eval_one(args[0]))
    else:
        return func.Func.Return(eval.eval_one(ast.Call([ast.Symbol("_"), *args])))

def _import(arg):
    import importlib
    mod = importlib.import_module(str(arg))
    context.cur_ctx.update(vars(mod))
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
          opexpr = before + [ast.Call([opexpr[i], opexpr[i-1], opexpr[i+1]])] + after
          found = True
          #print(opexpr)
          break
  if(callable(eval.eval_one(opexpr[0]))):
    return eval.eval_one(ast.Call(opexpr))
  return eval.eval_one(opexpr[0])

def _defstruct(*args):
    import ctypes
    name = str(args[0][0])
    members = args[0][1:]
    fields = []
    for m in members:
        if(str(m[1]) == "int"):
            fields.append((str(m[2]), ctypes.c_int))
    
    context.cur_ctx.update({
        "LOL::" + name : context.Context()
    })
    class DefStruct(ctypes.Structure):
        _fields_ = fields
    def _def(*args):
        if len(args) == 1:
            context.cur_ctx.update({
                str(args[0]) : DefStruct(),
                str(args[0]) + "::type" : ast.Symbol(name),
            })
            context.cur_ctx.update({
                "LOL::" + str(args[0]) : context.Context()
            })
            context.cur_ctx["LOL::" + str(args[0])].update({
                "value" : DefStruct(),
                "type" : ast.Symbol(name),
            })
            #print(context.cur_ctx)
        else:
            raise Exception("WRONG DEFINE FORM" + str([*args]))
        return None
    context.cur_ctx.update({
        name : func.PyMacro(_def)
    })
    context.cur_ctx["LOL::" + name].update({
        "def" : func.PyMacro(_def)
    })
    def _get(memb):
        return lambda *args: getattr(args[0], memb)
    def _set(memb):
        return lambda *args: setattr(args[0], memb, args[1])
    for m in members:
        context.cur_ctx.update({
            name + "::get_" + str(m[2]) : func.PyFunc(_get(str(m[2]))),
            name + "::set_" + str(m[2]) : func.PyFunc(_set(str(m[2]))),
        })
        context.cur_ctx["LOL::" + name].update({
            "get_" + str(m[2]) : func.PyFunc(_get(str(m[2]))),
            "set_" + str(m[2]) : func.PyFunc(_set(str(m[2]))),
        })
    #print(context.cur_ctx)

def _scope(arg1, arg2):
  if isinstance(arg2, ast.Call):
    return ast.Call([context.cur_ctx["LOL::"+arg1][arg2[0]]] + arg2[1:])
  return context.cur_ctx["LOL::"+ str(arg1)][str(arg2)]

def _dot(arg1, arg2):
  arg1_type = context.cur_ctx["LOL::"+ str(arg1)]["type"]
  if isinstance(arg2, ast.Call):
    return eval.eval_one(ast.Call([_scope(arg1_type, arg2[0]), arg1] + arg2[1:]))
  return eval.eval_one(ast.Call([_scope(arg1_type, arg2), arg1]))

def _block(*args):
  prev_ctx = context.cur_ctx
  context.cur_ctx =  context.Context({}, prev_ctx)
  for a in args:
    eval.eval_one(a)
  context.cur_ctx = prev_ctx
  return None

def _set(arg1, arg2):
  context.cur_ctx[str(arg1)] = eval.eval_one(arg2)

prelude_ctx = context.Context({
    "_" : func.PyMacro(_),
    "print" : func.PyFunc(_print),
    "int" : func.PyMacro(_defint),
    "var" : func.PyMacro(_defvar),
    "fn" : func.PyMacro(_fn),
    "macro" : func.PyMacro(_macro),
    "if" : func.PyFunc(_if),
    "return" : func.PyMacro(_ret),
    "import" : func.PyMacro(_import),
    "struct" : func.PyMacro(_defstruct),
    "$" : func.PyFunc(eval.eval_all),
    "block" : func.PyMacro(_block),
    "::" : func.PyMacro(_scope),
    "." : func.PyMacro(_dot),
    "=" : func.PyMacro(_set),
    "+" : func.BOp(operator.add),
    "-" : func.BOp(operator.sub),
    "*" : func.BOp(operator.mul),
    "!" : func.BOp(operator.not_),
    "~" : func.BOp(operator.inv),
    "<" : func.BOp(operator.lt),
    ">" : func.BOp(operator.gt),
    "<=" : func.BOp(operator.le),
    ">=" : func.BOp(operator.ge),
    "==" : func.BOp(operator.eq),
    "!=" : func.BOp(operator.ne),
    "||" : func.BOp(operator.or_),

    "true" : True,
    "false" : False,
})

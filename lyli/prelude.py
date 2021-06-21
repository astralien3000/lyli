import lyli.context as context
import lyli.ast as ast
import lyli.func as func
import lyli.eval as eval
import lyli.type

import operator

def _print(args):
    print(args.val)

def _print_bool(arg):
    if arg:
      print("true")
    else:
      print("false")

def _let(*args):
    if isinstance(args[0], ast.Call) and str(args[0][0]) == '=':
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

def _fn2(symbol):
  def _fn_args(*args):
    params = [(x[0] if isinstance(x, ast.Call) else x) for x in args]
    params_types = [(x[1] if isinstance(x, ast.Call) else None) for x in args]
    def _fn_args_ret(ret):
      def _fn_args_ret_expr(expr):
        #print((str(symbol), [str(p) for p in params], [str(p) for p in params_types], str(ret), str(expr)))
        context.cur_ctx.update({
            str(symbol) : func.Func2(ret, params_types, params, expr, context.cur_ctx)
        })
        #print(context.cur_ctx)
      return func.PyMacro(_fn_args_ret_expr)
    def _fn_args_void():
      return _fn_args_ret(None)
    return func.PolymorphicMacro([
        func.TypedPyMacro(["ast.Symbol"], _fn_args_ret),
        func.TypedPyMacro([], _fn_args_void),
    ])
  return func.PyMacro(_fn_args)

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
    if arg.val:
        return func.PyMacro(lambda a: eval.eval_one(a))
    return func.PyMacro(lambda a: None)

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
  #print("_ : " + str(args))
  opexpr = [*args]
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
        return lambda obj: lyli.type.Object(getattr(obj, memb), "int")
    def _set(memb):
        return lambda obj,val: setattr(obj, memb, val.val)
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
  fn = None
  args = []
  if isinstance(arg2, ast.Call):
    fn = _scope(arg1_type, arg2[0])
    args = [arg1] + arg2[1:]
  else:
    fn = _scope(arg1_type, arg2)
    args = [arg1]
  return fn(*args)

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
    
    "print" : func.PolymorphicFunc([
      func.TypedPyFunc(["bool"], _print_bool),
      func.TypedPyFunc(["int"], _print),
      func.TypedPyFunc(["float"], _print),
      func.TypedPyFunc(["str"], _print),
      func.TypedPyFunc(["char"], _print),
      func.TypedPyFunc(["type"], _print),
      func.TypedPyFunc(["call"], _print),
      func.TypedPyFunc(["ast.Call"], _print),
    ]),
    
    "let" : func.PyMacro(_let),
    "fn" : func.PyMacro(_fn),
    "macro" : func.PyMacro(_macro),
    "if" : func.PyFunc(_if),
    "return" : func.PyMacro(_ret),
    "import" : func.PyMacro(_import),
    "struct" : func.PyMacro(_defstruct),
    "$" : func.PyMacro(eval.eval_all),
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

    "typeof" : func.PyFunc(func.typeof),

    "true" : lyli.type.Object(True, "bool"),
    "false" : lyli.type.Object(False, "bool"),
    
    "type" : lyli.type.Object("type", "type"),
    "bool" : lyli.type.Object("bool", "type"),
    
    "int" : lyli.type.Object("int", "type"),
    "float" : lyli.type.Object("float", "type"),
    "char" : lyli.type.Object("char", "type"),
    "str" : lyli.type.Object("str", "type"),

    "ast.Call" : lyli.type.Object("ast.Call", "type"),
    "ast.Symbol" : lyli.type.Object("ast.Symbol", "type"),

    "func.Func" : lyli.type.Object("func.Func", "type"),
    "func.PyFunc" : lyli.type.Object("func.PyFunc", "type"),
    "func.BOp" : lyli.type.Object("func.BOp", "type"),
    "func.Macro" : lyli.type.Object("func.Macro", "type"),
    "func.PyMacro" : lyli.type.Object("func.PyMacro", "type"),
    "func.PolymorphicFunc" : lyli.type.Object("func.PyMacro", "type"),

    "FN" : func.TypedPyMacro(["ast.Symbol"], _fn2),
    
})

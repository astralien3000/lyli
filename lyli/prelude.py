import lyli.context as context
import lyli.ast as ast
import lyli.func as func
import lyli.eval as eval
import lyli.type

import operator

def _print(arg):
    print(arg.val)

def _print_pair(pair):
    print("pair({},{})".format(str(pair.val[0]), str(pair.val[1])))

def _print_none(n):
    print()

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

def _std_let(symbol, eq, value):
  assert(str(eq) == "=")
  context.cur_ctx.update({str(symbol) : value})

def _typed_let(symbol, colon, type, eq, value):
  assert(str(eq) == "=")
  assert(str(colon) == ":")
  context.cur_ctx.update({str(symbol) : value})

def _fn(*args):
  params = [ast.Call([x[1], x[3]]) if isinstance(x, ast.Call) else x for x in args]
  def _fn_args_expr(exp):
    #print(([str(p) for p in params], str(exp)))
    return eval.eval_one(ast.Call([ast.Call([ast.Call([ast.Call([ast.Symbol("FN")])] + params)]), exp]))
  return func.PyMacro(_fn_args_expr)

def _LET(symbol):
  def _let_type(T):
    def _let_type_val(val):
      #print((str(symbol), str(T), str(val)))
      context.cur_ctx.update({str(symbol) : val})
    return func.PyFunc(_let_type_val)
  def _let_none():
    return _let_type(None)
  return func.PolymorphicMacro([
    func.TypedPyMacro(["ast.Symbol"], _let_type),
    func.TypedPyMacro([], _let_none),
  ])

def _FN(symbol):
  def _fn_args(*args):
    params = [(x[0] if isinstance(x, ast.Call) else x) for x in args]
    params_types = [(x[1] if isinstance(x, ast.Call) else None) for x in args]
    def _fn_args_ret(ret):
      def _fn_args_ret_expr(*exprs):
        exp = ast.Call([ast.Symbol("block"), *exprs])
        #print((str(symbol), [str(p) for p in params], [str(p) for p in params_types], str(ret), str(exp)))
        f = func.Func2(ret, params_types, params, exp, context.cur_ctx)
        context.cur_ctx.update({
            str(symbol) : f
        })
        #print(context.cur_ctx)
        return f
      return func.PyMacro(_fn_args_ret_expr)
    def _fn_args_none():
      return _fn_args_ret(None)
    return func.PolymorphicMacro([
        func.TypedPyMacro(["ast.Symbol"], _fn_args_ret),
        func.TypedPyMacro([], _fn_args_none),
    ])
  return func.PyMacro(_fn_args)

def _FN_anon():
  return _FN(None)

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

def _if(cond):
    if cond.val:
      return func.PyMacro(lambda a: eval.eval_one(a))
    else:
      return func.PyMacro(lambda a: lyli.type.Object(None, "NoneType"))

def _IF(cond):
    def _IF_then(*then_exprs):
      def _IF_then_else(*else_exprs):
        then_exp = ast.Call([ast.Symbol("block"), *then_exprs]) 
        else_exp = ast.Call([ast.Symbol("block"), *else_exprs]) 
        #print((str(cond), str(then_exp), str(else_exp)))
        return eval.eval_one(then_exp if cond.val else else_exp)
      return func.PyMacro(_IF_then_else)
    return func.PyMacro(_IF_then)

def _ret(*args):
    if len(args) == 1:
        return func.Func.Return(eval.eval_one(args[0]))
    else:
        return func.Func.Return(eval.eval_one(ast.Call([ast.Symbol("_"), *args])))

def _(*args):
  print("_ : " + str(args))
  opexpr = [*args]
  for op in ["::",".","*","/","+","-","<","==","=",":"]:
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
          print(opexpr)
          break
  if(callable(eval.eval_one(opexpr[0]))):
    return eval.eval_one(ast.Call(opexpr))
  return eval.eval_one(opexpr[0])

def _stmt_simple(*args):
  if(len(args) == 1):
    #print("_stmt_simple LEN1 : " + str([*args][0]))
    return [*args][0]
  if(len(args) == 2):
    #print("_stmt_simple LEN2 : " + str([str(x) for x in args]))
    return ast.Call([*args])
  else:
    print("_stmt_simple ERR : " + str([str(x) for x in args]))
    raise "ERR"

def _stmt_op(*args):
  ops = ["::",".","*","/","+","-","<","==","=",":"]
  if(len(args) >= 3 and str(args[1]) in ops):
    return _stmt_op(ast.Call([args[1], args[0], args[2]]), *args[3:])
  else:
    return _stmt_simple(*args)

def _stmt_let(*args):
  if(str(args[0]) == "let"):
    if(str(args[2]) == "="):
      return _stmt_simple(ast.Call([ast.Call([ast.Call([ast.Symbol("LET"), args[1]])]), ast.Call([ast.Symbol("_"), *args[3:]])]))
    elif(str(args[2]) == ":"):
      assert(str(args[4]) == "=")
      return _stmt_simple(ast.Call([ast.Call([ast.Call([ast.Symbol("LET"), args[1]]), args[3]]), ast.Call([ast.Symbol("_"), *args[5:]])]))
    else:
      raise "ERR"
  else:
    return _stmt_op(*args)

def _stmt_fn(*args):
  if(str(args[0]) == "fn"):
    if(len(args) == 2):
      symbol = args[1][0][0]
      params = [ast.Call([x[1], x[3]]) if isinstance(x, ast.Call) else x for x in args[1][0][1:]]
      exp = args[1][1:]
      return _stmt_simple(ast.Call([ast.Call([ast.Call([ast.Call([ast.Symbol("FN"), symbol])] + params)]), *exp]))
    elif(len(args) == 4 and str(args[2]) == "->"):
      symbol = args[1][0]
      params = [ast.Call([x[1], x[3]]) if isinstance(x, ast.Call) else x for x in args[1][1:]]
      ret = args[3][0]
      exp = args[3][1:]
      return _stmt_simple(ast.Call([ast.Call([ast.Call([ast.Call([ast.Symbol("FN"), symbol])] + params), ret]), *exp]))
    else:
      raise "ERR"
  elif(len(args) >= 2 and str(args[1]) == "->" and isinstance(args[0], ast.Call) and str(args[0][0]) == "fn"):
    #print(str([str(x) for x in args]))
    params = [ast.Call([x[1], x[3]]) if isinstance(x, ast.Call) else x for x in args[0][1:]]
    ret = args[2][0]
    exp = args[2][1:]
    return _stmt_simple(ast.Call([ast.Call([ast.Call([ast.Call([ast.Symbol("FN")])] + params), ret]), *exp]))
  else:
    return _stmt_let(*args)

def _stmt_if(*args):
  if(isinstance(args[0], ast.Call) and isinstance(args[0][0], ast.Call) and str(args[0][0][0]) == "if"):
    if(len(args) == 2 and isinstance(args[1], ast.Call) and str(args[1][0]) == "else"):
      cond = args[0][0][1]
      then_exp = args[0][1:]
      else_exp = args[1][1:]
      return _stmt_simple(ast.Call([ast.Call([ast.Call([ast.Symbol("IF"), cond]), *then_exp]), *else_exp]))
    else:
      raise "ERR"
  else:
    return _stmt_fn(*args)

def _stmt(*args):
  #print("_ : " + str([str(x) for x in args]))
  return eval.eval_one(_stmt_if(*args))

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
  ret = None
  for a in args:
    ret = eval.eval_one(a)
  context.cur_ctx = prev_ctx
  return ret

def _set(arg1, arg2):
  context.cur_ctx[str(arg1)] = eval.eval_one(arg2)

def _Fn(*args):
  #print("_Fn : " + str(args))
  fnargs = "Fn({})".format(",".join([str(x.val) for x in args]))
  def _Fn_ret(ret):
    fnargsret = "{}({})".format(fnargs, str(ret.val))
    #print(fnargsret)
    return lyli.type.Object(fnargsret, "type")
  def _Fn_noret():
    fnargsret = "{}()".format(fnargs)
    #print(fnargsret)
    return lyli.type.Object(fnargsret, "type")
  return func.PolymorphicFunc([
    func.TypedPyFunc(["type"], _Fn_ret),
    func.TypedPyFunc([], _Fn_noret),
  ])

def _quote(arg):
  return arg

def _Pair(lt, rt):
  ret = "Pair({},{})".format(lt,rt)
  return lyli.type.Object(ret, "type")

def _pair(l, r):
  return lyli.type.Object((l,r), _Pair(l.type, r.type))

def _left(p):
  return p.val[0]

def _right(p):
  return p.val[1]

prelude_ctx = context.Context({
    "_" : func.PyMacro(_stmt),
    
    "print" : func.PolymorphicFunc([
      func.TypedPyFunc(["bool"], _print_bool),
      func.TypedPyFunc(["int"], _print),
      func.TypedPyFunc(["float"], _print),
      func.TypedPyFunc(["str"], _print),
      func.TypedPyFunc(["char"], _print),
      func.TypedPyFunc(["type"], _print),
      func.TypedPyFunc(["call"], _print),
      func.TypedPyFunc(["ast.Symbol"], _print),
      func.TypedPyFunc(["ast.Call"], _print),
      func.TypedPyFunc(["NoneType"], _print_none),
      func.TypedPyFunc(["Pair(ast.Symbol,ast.Symbol)"], _print_pair),
    ]),
    
    "let" : func.PyMacro(_let),
    "fn" : func.PyMacro(_fn),
    "macro" : func.PyMacro(_macro),
    "quote" : func.PyMacro(_quote),
    "if" : func.PyFunc(_if),
    "return" : func.PyMacro(_ret),
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
    "<" : func.BOp(operator.lt, "bool"),
    ">" : func.BOp(operator.gt, "bool"),
    "<=" : func.BOp(operator.le, "bool"),
    ">=" : func.BOp(operator.ge, "bool"),
    "==" : func.BOp(operator.eq, "bool"),
    "!=" : func.BOp(operator.ne, "bool"),
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

    "NoneType" : lyli.type.Object("NoneType", "type"),

    "ast.Call" : lyli.type.Object("ast.Call", "type"),
    "ast.Symbol" : lyli.type.Object("ast.Symbol", "type"),

    "func.Func" : lyli.type.Object("func.Func", "type"),
    "func.PyFunc" : lyli.type.Object("func.PyFunc", "type"),
    "func.BOp" : lyli.type.Object("func.BOp", "type"),
    "func.Macro" : lyli.type.Object("func.Macro", "type"),
    "func.PyMacro" : lyli.type.Object("func.PyMacro", "type"),
    "func.PolymorphicFunc" : lyli.type.Object("func.PyMacro", "type"),

    "FN" : func.PolymorphicMacro([
      func.TypedPyMacro(["ast.Symbol"], _FN),
      func.TypedPyMacro([], _FN_anon),
    ]),
    
    "LET" : func.TypedPyMacro(["ast.Symbol"], _LET),
    "IF" : func.PyFunc(_IF),
    
    "Fn" : func.PyFunc(_Fn),

    "Pair" : func.PyFunc(_Pair),
    "pair" : func.PyFunc(_pair),
    "left" : func.PyFunc(_left),
    "right" : func.PyFunc(_right),

})

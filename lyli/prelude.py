import lyli.context as context
import lyli.func as func
import lyli.eval as eval
import lyli.ast as ast


def _file(ctx, *args):
  ret = None
  for arg in args:
    ctx, ret = eval.eval(ctx, arg)
  return ctx, ret


def _stmt(ctx, *args):
  S = ast.Symbol
  C = ast.Call
  match args:
    case [S("let"), S(var_name), S("="), *val_exprs]:
      print(f"LET {var_name} = {val_exprs}")
    case [S("print"), *val_exprs]:
      print("PRINT")
    case [S("fn"), C([S(func_name), *func_args])]:
      print(f"FN {func_name}")
    case [S("fn"), C([C([S(func_name), *func_args]), *func_exprs])]:
      print(f"FN2 {func_name}")
    case [S("fn"), C([S(func_name), *func_args]), S("->"), C([func_ret_type, *func_exprs])]:
      print(f"FN3 {func_name}")
  return ctx, None
  # return eval.eval(
  #   ctx,
  #   ast.Call(
  #     ast.Symbol(f"stmt.{args[0]}"),
  #     *args[1:],
  #   )
  # )


def _stmt_let(ctx, *args):
  [let_symbol, eq_op, let_value, *others] = args
  assert(isinstance(eq_op, ast.Symbol))
  assert(eq_op.name == "=")
  assert(len(others) == 0)
  new_ctx = context.Context(ctx, {
    let_symbol.name: let_value
  })
  return new_ctx, None


def _stmt_fn(ctx, *args):
  [[fn_symbol, *fn_args], arrow_op, [fn_ret_type, *fn_body], *others] = args
  assert(isinstance(fn_symbol, ast.Symbol))
  assert(isinstance(arrow_op, ast.Symbol))
  assert(arrow_op.name == "->")
  assert(len(others) == 0)
  fn_arg_symbols = [
    fn_arg_symbol
    for [stmt_symbol, fn_arg_symbol, typehint_op, fn_arg_type] in fn_args
  ]
  new_ctx = context.Context(ctx)
  f = func.LyliFunc(fn_arg_symbols, fn_body, new_ctx)
  new_ctx[fn_symbol.name] = f
  return new_ctx, f


prelude_ctx = context.Context({
  "file": func.PyMacro(_file),
  "stmt": func.PyMacro(_stmt),

  "print": func.PyFunc(print),
})

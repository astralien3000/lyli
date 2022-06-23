import lyli.context as context
import lyli.func as func
import lyli.eval as eval
import lyli.ast as ast


S = ast.Symbol
C = ast.Call


def _file(ctx, *args):
  ret = None
  for arg in args:
    ctx, ret = eval.eval(ctx, arg)
  return ctx, ret


class Stmt:
  matchers = []

  @staticmethod
  def matcher(function):
    Stmt.matchers.append(function)
    return function
  
  @staticmethod
  def final(matchers, ctx, *args):
    raise Exception(
      f"Could not match {args}"
    )

  @staticmethod
  def stmt(ctx, *args):
    return Stmt.matchers[0](
      [*Stmt.matchers[1:], Stmt.final],
      ctx,
      *args
    )


@Stmt.matcher
def _stmt_let(matchers, ctx, *args):
  match args:
    case [S("let"), S(var_name), S("="), val_expr]:
      ctx, value = eval.eval(ctx, val_expr)
      new_ctx = context.Context(ctx, {
        var_name: value,
      })
      return new_ctx, None
  return matchers[0](matchers[1:], ctx, *args)


@Stmt.matcher
def _stmt_print(matchers, ctx, *args):
  match args:
    case [S("print"), *val_exprs]:
      print(*val_exprs)
      return ctx, None
  return matchers[0](matchers[1:], ctx, *args)


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
  "stmt": func.PyMacro(Stmt.stmt),

  "print": func.PyFunc(print),
})

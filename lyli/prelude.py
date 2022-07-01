import lyli.context as context
import lyli.func as func
import lyli.eval as eval
import lyli.ast as ast

import operator as op


S = ast.Symbol
C = ast.Call


def _file(ctx, *args):
  ret = None
  for arg in args:
    ctx, ret = eval.eval(ctx, arg)
  return ctx, ret


class Stmt:

  class Next:

    def __init__(self, matchers, ctx, *args):
      self.matchers = matchers
      self.ctx = ctx
      self.args = args

    def __call__(self):
      if len(self.matchers) == 0:
        raise Exception(
          f"Could not match {self.args}"
        )
      else:
        return self.matchers[0](
          Stmt.Next(
            self.matchers[1:],
            self.ctx,
            *self.args,
          ),
          self.ctx,
          *self.args,
        )

  def __init__(self, matchers = []):
    self.matchers = matchers

  def matcher(self, function):
    self.matchers.append(function)
    return function

  def __call__(self, ctx, *args):
    return Stmt.Next(
      self.matchers,
      ctx,
      *args,
    )()


_stmt = Stmt()


@_stmt.matcher
def _stmt_let(next, ctx, *args):
  match args:
    case [S("let"), S(var_name), S("="), val_expr]:
      ctx, value = eval.eval(ctx, val_expr)
      new_ctx = context.Context(ctx, {
        var_name: value,
      })
      return new_ctx, None
  return next()


@_stmt.matcher
def _stmt_print(next, ctx, *args):
  match args:
    case [S("print"), *val_exprs]:
      return eval.eval(ctx, C([S("print"), *val_exprs]))
  return next()


def arg_names(*fn_args):
  ret = []
  for arg in fn_args:
    match arg:
      case S(arg_name):
        ret.append(arg_name)
      case C([S("stmt"), S(arg_name), S(":"), arg_type]):
        ret.append(arg_name)
  return ret


@_stmt.matcher
def _stmt_fn(next, ctx, *args):
  match args:
    case [S("fn"), C([S(fn_name), *fn_args]), S("->"), C([fn_ret_type, *fn_body])]:
      new_ctx = context.Context(ctx)
      f = func.LyliFunc(arg_names(*fn_args), fn_body, new_ctx)
      new_ctx[fn_name] = f
      return new_ctx, f
    case [S("fn"), C([C([S(fn_name), *fn_args]), *fn_body])]:
      new_ctx = context.Context(ctx)
      f = func.LyliFunc(arg_names(*fn_args), fn_body, new_ctx)
      new_ctx[fn_name] = f
      return new_ctx, f
  return next()


@_stmt.matcher
def _stmt_op(next, ctx, *args):
  match args:
    case [left_expr, S(op_name), right_expr]:
      return eval.eval(ctx, C([S(op_name), left_expr, right_expr]))
  return next()


@_stmt.matcher
def _stmt_if(next, ctx, *args):
  match args:
    case [C([C([S("if"), cond_expr]), if_body]), C([S("else"), else_body])]:
      _, cond_val = eval.eval(ctx, cond_expr)
      if cond_val:
        return eval.eval(ctx, if_body)
      else:
        return eval.eval(ctx, else_body)
  return next()


prelude_ctx = context.Context({
  "file": func.PyMacro(_file),
  "stmt": func.PyMacro(_stmt),

  "print": func.PyFunc(print),

  "+": func.PyFunc(op.add),
  "-": func.PyFunc(op.sub),

  "*": func.PyFunc(op.mul),
  "/": func.PyFunc(op.truediv),
  "%": func.PyFunc(op.mod),

  "$": func.PyFunc(lambda x: x),

  "==": func.PyFunc(op.eq),
  "<=": func.PyFunc(op.le),
  ">=": func.PyFunc(op.ge),
  "<": func.PyFunc(op.lt),
  ">": func.PyFunc(op.gt),

  "quote": func.PyMacro(lambda ctx, arg: (ctx, arg)),

  "pair": func.PyFunc(lambda l, r: (l, r)),
  "left": func.PyFunc(lambda p: p[0]),
  "right": func.PyFunc(lambda p: p[1]),

  "typeof": func.PyFunc(lambda arg: None),

})

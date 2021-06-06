import subprocess

import lyli.expr_tree as expr_tree
import lyli.context as context
import lyli.func as func
import lyli.eval as eval

def get_python_cflags():
  python_config_process = subprocess.run(["python3-config", "--cflags"], capture_output=True)
  python_config_raw = str(python_config_process.stdout.replace(b'\n', b' ').decode("utf-8")).split(" ")
  return list(filter(lambda x: len(x) > 0, python_config_raw))

def get_python_ldflags():
  python_config_process = subprocess.run(["python3-config", "--ldflags", "--embed"], capture_output=True)
  python_config_raw = str(python_config_process.stdout.replace(b'\n', b' ').decode("utf-8")).split(" ")
  return list(filter(lambda x: len(x) > 0, python_config_raw))

def compile_main(fn):
  with open("main.c", "w+") as f:
    f.write(gen_main(fn))
  subprocess.run(["gcc", "-fPIE", "-c", "main.c", "-o", "main.o"] + get_python_cflags())
  subprocess.run(["gcc", "main.o", "-o", "main"] + get_python_ldflags())
  
def gen_main(fn):
  code  = """
#include <Python.h>

PyObject * preludeName = NULL;

PyObject * preludeModule = NULL;

PyObject * _printFunc = NULL;

"""
  code += gen_func("lyli_main", fn)
  code += """

int main() {
  Py_Initialize();
  preludeName = PyUnicode_DecodeFSDefault("lyli.prelude");
  preludeModule = PyImport_Import(preludeName);
  _printFunc = PyObject_GetAttrString(preludeModule, "_print");
  lyli_main();
  return 0;
}
"""
  return code

def gen_func(name, fn):
  code = ""
  if fn.restype:
    code += str(fn.restype)
  else:
    code += "void"
  code += " "
  code += str(name)
  code += "("
  for p in fn.params:
      code += p.type + " " + p
  code += ")"
  code += "{"
  for e in fn.exp:
    code += gen_expr(e)
  code += "}"
  return code

def gen_expr(x):
  if isinstance(x, expr_tree.Symbol):
    return context.cur_ctx[str(x)]
  elif isinstance(x, expr_tree.Atomic):
    return str(x.val)
  elif isinstance(x, expr_tree.Call):
    return gen_call(x)
  elif isinstance(x, expr_tree.Expr):
    raise TypeError("not (yet) supported : " + str(type(x)) + " (" + str(x) + ")")
  else:
    return x

def gen_call(x):
  fn = eval.eval_one(x[0])
  if isinstance(fn, func.PyFunc):
    return gen_pyfunc_call(fn, x[1:])
  else:
    return "/*not supported*/"

def gen_pyfunc_call(f, args):
  print(f)
  print(args)
  args_str = "("
  args_vals = []
  for a in args:
    if isinstance(a, expr_tree.Integer):
      args_str += "i"
      args_vals.append(str(a.val))
    elif isinstance(a, expr_tree.String):
      args_str += "s"
      args_vals.append('"' + a.val + '"')
    else:
      print("Not implemented : " + str(a))
      return "/*Not implemented*/"
  args_str += ")"
  ret  = '{'
  ret += 'PyGILState_STATE gstate;'
  ret += 'gstate = PyGILState_Ensure();'
  ret += 'PyObject* arglist = 0;'
  ret += 'PyObject* result = 0;'
  ret += 'arglist = Py_BuildValue("'+args_str+'", '+','.join(args_vals)+');'
  ret += 'result = PyEval_CallObject('+f.func.__name__+'Func, arglist);'
  ret += 'Py_DECREF(arglist);'
  ret += 'Py_DECREF(result);'
  ret += 'PyGILState_Release(gstate);'
  ret += '}'
  return ret
  
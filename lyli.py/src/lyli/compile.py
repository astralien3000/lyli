import subprocess
import os

import lyli.ast as ast
import lyli.context as context
import lyli.func as func
import lyli.eval as eval
import lyli.prelude as prelude

def get_cache_dir():
  ret = os.path.join(".", "__lycache__")
  if not os.path.exists(ret):
    os.makedirs(ret)
  return ret

def get_python_cflags():
  python_config_process = subprocess.run(["python3-config", "--cflags"], capture_output=True)
  python_config_raw = str(python_config_process.stdout.replace(b'\n', b' ').decode("utf-8")).split(" ")
  return list(filter(lambda x: len(x) > 0, python_config_raw))

def get_python_ldflags():
  python_config_process = subprocess.run(["python3-config", "--ldflags", "--embed"], capture_output=True)
  python_config_raw = str(python_config_process.stdout.replace(b'\n', b' ').decode("utf-8")).split(" ")
  return list(filter(lambda x: len(x) > 0, python_config_raw))

def compile_main(fn):
  c_path = os.path.join(get_cache_dir(), "main.c")
  o_path = os.path.join(get_cache_dir(), "main.o")
  with open(c_path, "w+") as f:
    f.write(gen_main(fn))
  subprocess.run(["gcc", "-fPIE", "-c", c_path, "-o", o_path] + get_python_cflags())
  subprocess.run(["gcc", o_path, "-o", "main"] + get_python_ldflags())
  
def gen_main(fn):
  return f"""
    #include <Python.h>

    PyObject * preludeName = NULL;

    PyObject * preludeModule = NULL;

    PyObject * _old_printFunc = NULL;

    {gen_func("lyli_main", fn)}

    int main() {{
      Py_Initialize();
      preludeName = PyUnicode_DecodeFSDefault("lyli.prelude");
      preludeModule = PyImport_Import(preludeName);
      _old_printFunc = PyObject_GetAttrString(preludeModule, "_old_print");
      lyli_main();
      return 0;
    }}
  """

def gen_func(name, fn):
  return f"""
    {str(fn.restype) if fn.restype else "void"}
    {str(name)}
    ({", ".join([
      f"{p.typ} {p}"
      for p in fn.params
    ])})
    {{
    {gen_expr(fn.exp)}
    }}
  """

def gen_expr(x):
  if isinstance(x, ast.Symbol):
    return context.cur_ctx[str(x)]
  elif isinstance(x, ast.Atomic):
    return str(x.val)
  elif isinstance(x, ast.Call):
    return gen_call(x)
  elif isinstance(x, ast.Expr):
    raise TypeError("not (yet) supported : " + str(type(x)) + " (" + str(x) + ")")
  else:
    return x

def gen_call(x):
  fn = eval.eval_one(x[0])
  if isinstance(fn, func.PyMacro):
    return gen_pymacro_call(fn, x[1:])
  elif isinstance(fn, func.PyFunc):
    return gen_pyfunc_call(fn, x[1:])
  else:
    return "/*not supported*/"

def gen_pymacro_call(f, args):
  if f == prelude.prelude_ctx["block"]:
    ret = ""
    for arg in args:
      ret += gen_call(arg)
    return ret
  return "/*not supported*/"

def gen_pyfunc_call(f, args):
  print(f)
  print(args)
  args_str = "("
  args_vals = []
  for a in args:
    if isinstance(a, ast.Integer):
      args_str += "i"
      args_vals.append(str(a.val))
    elif isinstance(a, ast.String):
      args_str += "s"
      args_vals.append('"' + a.val + '"')
    else:
      print("Not implemented : " + str(a))
      return "/*Not implemented*/"
  args_str += ")"
  return f'''
    {{
      PyGILState_STATE gstate;
      gstate = PyGILState_Ensure();
      PyObject* arglist = 0;
      PyObject* result = 0;
      arglist = Py_BuildValue("{args_str}", {','.join(args_vals)});
      result = PyObject_CallObject({f.func.__name__}Func, arglist);
      Py_DECREF(arglist);
      Py_DECREF(result);
      PyGILState_Release(gstate);
    }}
  '''
  return ret
  
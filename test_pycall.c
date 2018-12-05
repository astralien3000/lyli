#include <Python.h>

#include <stdio.h>

void test(void) {
    PyObject* arglist = 0;
    PyObject* result = 0;

    arglist = Py_BuildValue("(s)", "hello");

    printf("%p, %p\n", &print, arglist);

    PyGILState_STATE gstate;
    gstate = PyGILState_Ensure();
    
    result = PyEval_CallObject(&print, arglist);
    
    PyGILState_Release(gstate);

    Py_DECREF(arglist);
}

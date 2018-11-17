#!/usr/bin/python

from cgen import *
from subprocess import call
from ctypes import *

test = FunctionBody(
    FunctionDeclaration(Value("int", "test"), [Value("int", "a"),Value("int", "b")]),
    Block([Statement("return a+b")])
)

f = open("test.c", "w+")
f.write(str(test))
f.close()

call(["gcc", "-shared", "-fPIC", "test.c", "-o", "test.so"])

test_so = CDLL("./test.so")

print(test_so.test(4,4))

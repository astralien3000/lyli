from subprocess import call
from ctypes import *

def myprint(args):
    print args

print(myprint)
myprint(666)

cmd  = ["gcc", "-shared", "-fPIC", "test_pycall.c", "-o", "test_pycall.so"]
cmd += ["-I/usr/include/python2.7"]
cmd += ["-DLOOL="+hex(id(myprint))]

print(cmd)
call(cmd)

test_so = CDLL("./test_pycall.so")

test_so["test"]()

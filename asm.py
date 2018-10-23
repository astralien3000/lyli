#!/usr/bin/python

import ctypes, struct, time, math

from pycca.asm import *

msg = ctypes.create_string_buffer(b"Hello, world !\n")
fn = mkfunction([
    mov(rax, 0x1),   # write  (see unistd_64.h)
    mov(rdi, 1),   # stdout
    mov(rsi, ctypes.addressof(msg)),
    mov(rdx, len(msg)-1),
    syscall(),
    ret(),
])

fn.restype = ctypes.c_uint64

fn()

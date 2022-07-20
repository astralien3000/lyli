// "standard" form
fn add0(a, b) { a + b + 0x0 };
fn add1(a : int, b : int) { a + b + 0x1 };
fn add2(a, b) -> int { a + b + 0x2 };
fn add3(a : int, b : int) -> int { a + b + 0x3 };

// "anonymous" form
fn(a, b) { a + b };
fn(a : int, b : int) { a + b };
fn(a, b) -> int { a + b };
fn(a : int, b : int) -> int { a + b };

// "let" form
let add4 = fn(a, b) { a + b + 0x4 };
let add5 = fn(a : int, b : int) { a + b + 0x5 };
let add6 = fn(a, b) -> int { a + b + 0x6 };
let add7 = fn(a : int, b : int) -> int { a + b + 0x7 };

// "recursive-enabled let" form
let add8 = fn tmp(a, b) { a + b + 0x8 };

let add9 = fn tmp(a : int, b : int) { a + b + 0x9 };

let addA = fn tmp(a, b) -> int { a + b + 0xA };

let addB = fn tmp(a : int, b : int) -> int { a + b + 0xB };

// test
print(add0(1,1));
print(add1(1,1));
print(add2(1,1));
print(add3(1,1));
print(add4(1,1));
print(add5(1,1));
print(add6(1,1));
print(add7(1,1));
print(add8(1,1));
print(add9(1,1));
print(addA(1,1));
print(addB(1,1));

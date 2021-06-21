// "standard" form
//fn add0(a, b) { a + b };
//fn add1(a : int, b : int) { a + b };
//fn add2(a, b) -> int { a + b };
//fn add3(a : int, b : int) -> int { a + b };

// "let" form
//let add4 = fn(a, b) { a + b };
//let add5 = fn(a : int, b : int) { a + b };
//let add6 = fn(a, b) -> int { a + b };
//let add7 = fn(a : int, b : int) -> int { a + b };

// "recursive-enabled let" form
//let add8 = fn tmp(a, b) { a + b };
//let add9 = fn tmp(a : int, b : int) { a + b };
//let addA = fn tmp(a, b) -> int { a + b };
//let addB = fn tmp(a : int, b : int) -> int { a + b };

// "call" form
FN(addC)(a, b)()(a + b);
FN(addD)(a(int), b(int))()(a + b);
FN(addE)(a, b)(int)(a + b);
FN(addF)(a(int), b(int))(int)(a + b);

// test
//print(add0(1,1));
//print(add1(1,1));
//print(add2(1,1));
//print(add3(1,1));
//print(add4(1,1));
//print(add5(1,1));
//print(add6(1,1));
//print(add7(1,1));
//print(add8(1,1));
//print(add9(1,1));
//print(addA(1,1));
//print(addB(1,1));
print(addC(1,1));
print(addD(1,1));
print(addE(1,1));
print(addF(1,1));

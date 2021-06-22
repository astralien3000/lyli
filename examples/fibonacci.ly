
fn fib(n : int) -> int {
    IF(n < 2)(n)(fib(n-1) + fib(n-2))
};

print(fib(20));

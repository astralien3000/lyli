
fn fib(n : int) -> int {
    if(n < 2) {
      n
    }
    else {
      fib(n-1) + fib(n-2)
    }
};

print(fib(20));

# Functions

## The main function

```
fn main() {}
```

## Fully type-defined function

```
fn test(a : i32, b : i32) -> i32 {}
```

## Polymorphism

```
fn test(a : i32, b : i32) -> i32 { a };
fn test(a : u8, b : i32) -> u8 { a };
```

## Generic

```
fn test(a, b) { a }
```

## Recursive

```
fn fib(n) {
  if(n < 2) {
    n
  }
  else {
    fib(n-1) + fib(n-2)
  }
}
```

## Shadowing

### Polymorphism is a form of shadowing

```
fn test(a : i32, b : i32) -> i32 { a };
print(typeof(test));
fn test(a : u8, b : i32) -> u8 { a };
print(typeof(test));
```

```
fn(i32(i32,i8))
polymorphic_function(...TODO...)
```

```
let test = fn(a : i32, b : i32) -> i32 { a };
let test = polymorphic_function(test, fn test(a : u8, b : i32) -> u8 { a });
```

### Use of let form

```
fn test() { print("first") };
let test = fn() { print("second") };
```

Warning, this performs a reset on all polymorph versions of the function.

TODO : check conflicts with polymorphism

### Call previous impl

```
fn test() {
  print("first")
};

let test = fn() {
  test();
  print("second")
};
```

### Recursive + Call previous impl

```
fn fib(n) {
  if(n < 2) {
    n
  }
  else {
    fib(n-1) + fib(n-2)
  }
};

let fib = fn fib2(n) {
  if(n < 42) {
    fib(n)
  }
  else {
    print("Over 42 !");
    fib2(n-1) + fib2(n-2)
  }
};
```

TODO : is "fib2" available to context ?
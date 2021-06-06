# Variables

## Define

```
let x = 42;
print(x)
```

## Immutable by default

```
let x = 42;
print(x);
x = 666; // <- Error
print(x);
```

## Shadowing

```
let x = 1;
print(x);
let x = x + 1;
print(x);
let x = x * x;
print(x);
```

```
1
2
4
```

## Shadowing + type

```
let a = 1;
print(a);
let a = "hello";
print(a);
```

```
1
hello
```

## Shadowing in functions

```
let a = "global";

print(a);

fn test() {
  print(a);
  let a = "local";
  print(a);
};

print(a);

let a = "global again";

print(a);

test();

print(a);
```

```
global
global
global again
global
local
global again
```

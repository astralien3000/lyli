# Types

A type has basically a name and a size.

## typeof

```
let a = u32(5);
let Ta = typeof(a);
print(Ta);
let TTa = typeof(Ta);
print(TTa);
let TTTa = typeof(TTa);
print(TTTa);
```

```
u32
type
type
```

## bool

```
> true;
true
> false;
false
> typeof(false);
bool
```

## integers

### Classic

Unsigned integers : u8, u16, u32, u64
Signed integers : i8, i16, i32, i64

### Wide

For integers that don't fit in the previous types.
Still fits on the stack.
Static type (size defined by the `type)

```
template(n) {
  struct WideInteger {
    ???
  };
}
```

## floats

### Classic

f32, f64

### Wide

## strings

### string slices

see Rust !
also try to see Python...

## literals

```
> typeof(1);
generic_int
> typeof(1.0);
generic_float
> typeof("1");
generic_string
```

## Generic types

### Simple

```
let a = 1;
print(typeof(a));
let b = u32(1) + a;
print(typeof(b));
print(typeof(a));
```

```
generic_int
u32
u32
```

### Containers

```
let a = array[1,2,3,4,5];
print(typeof(a));
let b = u32(1) + a[0];
print(typeof(b));
print(typeof(a));
```

```
array(generic_int)
u32
array(u32)
```

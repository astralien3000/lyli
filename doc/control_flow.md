# Control flow

should look like C, mainly (if, else if, else, while, for)
also take a little from Python ? (for in ?, with ?)
also take a little from Rust (match ?)

## if, else if, else

```
if(cond) {
  ...
}
else if(cond) {
  ...
}
else {
  ...
}
```

can return a value

```
let a = if(cond) { 42 } else { 666 };
```

## while

```
while(cond) {
  ...
}
```

## for

```
for(init ; cond ; update) {
  ...
}
```

## foreach (python for...in)

TODO : discuss form

```
foreach(variable in iterable_container) {
  ...
}
```

OR

```
for(variable in iterable_container) {
  ...
}
```

OR

```
for variable in iterable_container {
  ...
}
```

OR something else ?

## do...while (???)

useless ???

## with (???)

similar to let (collision) ???

## match

like rust
replaces C/C++ switch

```
match variable {
  value1 : expr,
  value2 : {
    ...
  },
  ...
}
```

TODO : link with enums, variants
TODO : parenthesis or not ?
TODO : what about if let ?


# Introspection

need something powerful, and execution-time friendly (most computation done at compile-time)

## All

### typeof

```
let a = ...;
let t = typeof(a);
```

### sizeof

return the size on the stack

```
let a = ...;
let s = sizeof(a);
```

### quote

return symbol/expr

```
let a = ...;
let expr = quote(a);
```

## Modules

### Current module is "self"

### Get all public members

```
let members = get_members(module);
```

### Get public functions

```
let funcs = get_functions(module);
```

### Get public submodules

```
let modules = get_modules(module);
```

### Get name

Get real name (not local alias)

```
let name = get_name(module)
```

### Get code

Get AST

```
let expr = get_expr(module);
print(expr);
```

```
mod module (...)
```


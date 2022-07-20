# Modules

Should work kind-of like Python modules, because of the "compilation is execution" principle.

## Import

Import is used when code is written in an other file than the current one.

TODO : trigger of code execution ? (Once ? Eacht time ?)
```
import test;
import test; // ???
```

### Simple

```
import module;

...
module::function(...);
...
```

### Alias

```
let mod = import module;

...
mod::function(...);
...
```

### Bring in scope

```
let mod = import module;
let fun = mod::function;

...
fun(...);
...
```

## In-file modules

Should looke like rust.

mod block is not a scope, all defined objects are still alive after the block.

```
mod a {
  mod b {
    fn test() {}
  };
  fn test() {}
};
let c = mod {
  fn test() {}
}
```

WARNING : everythng is private by default.

## Make things public

pub block is not a scope, all defined objects are still alive after the block.

`test.ly`

```
pub fn fun1() {};

pub let a1 = 0;

fn fun2() {};

pub {
  fn fun3() {};
  fn fun4() {};
  let a2 = 0
};

mod mod1 {
  pub fn fun5()
};


pub mod mod2 {
  fn fun6();
  pub fn fun7()
};
```

```
import test;

test::fun1();     // Ok
test::a1;         // Ok
test::fun2();     // ERROR
test::fun3();     // Ok
test::fun4();     // Ok
test::a2;         // Ok
test::mod1;       // ERROR
test::mod1::fun5; // ERROR
test::mod2;       // Ok
test::mod2::fun6; // ERROR
test::mod2::fun7; // Ok
```

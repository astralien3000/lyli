# Variants

should behave like a Rust enum

name taken from C++ 17 std::variant

```
variant Message {
  Write(u32, String),
  Read(u32)
};
```

```
let msg = Message::Write(4, "test");

match msg {
  Message::Write(size, value) : {
    ...
  },
  Message::Read(size) : {
    ...
  }
};
```

## Option

like in Rust

```
let a = Some(5);
let b = None;
```


```
template(T) {
  variant Option {
    Some(T),
    None
  };
};
```

TODO : generic ???
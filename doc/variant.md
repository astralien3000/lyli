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


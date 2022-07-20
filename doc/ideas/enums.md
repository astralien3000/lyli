# Enums

should behave like C/C++ enums

conflicts with rust enums : see variants

```
enum MyEnum {
  MEMBER1,
  MEMBER2,
  MEMBER3,
  MEMBER4,
};
```

```
MyEnum::MEMBER1;
```

Can't define int value.

Can be converted to int ?

Behave more like C++ class enums.

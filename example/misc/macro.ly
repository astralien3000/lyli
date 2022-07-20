let i = 42;

macro mymacro (arg) {
    i = arg;
};

fn myfunc (arg : int) {
    i = arg;
};

print("---------- macro ----------");
print(i);
block {
  print(i);
  let i = 0;
  print(i);
  mymacro(666);
  print(i);
};
print(i);
print("---------- macro ----------");

print("---------- func ----------");
print(i);
block {
  print(i);
  let i = 0;
  print(i);
  myfunc(666);
  print(i);
};
print(i);
print("---------- func ----------");

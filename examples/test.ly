
fn miew(a : int) -> int {
  print(5);
  print(a);
  a * 10 + 42 * 10
};

fn loöl(a : int) -> int {
  if(a < 20) {
    print("UNDER 20 !");
    a
  }
  else {
    miew(a)
  }
};

print(loöl(10));
print(loöl(42));

struct Test {
  int a;
  int b;
  int c;
};

Test test;

test.set_a(666);
test.set_b($(test.get_a() + 1) * 10);

print(test.get_a());
print(test.get_b());
print(test.get_c());

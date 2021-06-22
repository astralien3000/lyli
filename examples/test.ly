
fn miew(a : int) -> int {
    a * 10 + 42 * 10
};

fn loöl(a : int) -> int {
    miew(a)
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

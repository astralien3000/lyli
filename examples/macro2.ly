
macro mymacro (arg) {
    print(arg);
};

fn void myfunc (int arg) {
    print(arg);
};

print("---------- macro ----------");
mymacro(1 + 1);
print("---------- macro ----------");

print("---------- func ----------");
myfunc(1 + 1);
print("---------- func ----------");

print("---------- func ----------");
myfunc{1 + 1};
print("---------- func ----------");

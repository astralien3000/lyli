
macro mymacro (arg) {
    print(arg);
};

fn myfunc (arg : int) {
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

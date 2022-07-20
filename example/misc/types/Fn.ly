let T1 = Fn()();
let T2 = Fn()(int);
let T3 = Fn(int,int)();
let T4 = Fn(int,int)(int);
let T5 = Fn(Fn(int)())(Fn(int)());

print(T1);
print(T2);
print(T3);
print(T4);
print(T5);

print(typeof(T1));
print(typeof(T2));
print(typeof(T3));
print(typeof(T4));
print(typeof(T5));

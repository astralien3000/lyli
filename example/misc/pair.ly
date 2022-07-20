let c = pair(quote(a), quote(b));

print(c);
print(typeof(c));
print(left(c));
print(typeof(left(c)));
print(right(c));
print(typeof(right(c)));

let d = pair(0,"right");

print(d);
print(typeof(d));
print(left(d));
print(typeof(left(d)));
print(right(d));
print(typeof(right(d)));

let e = pair(c,d);

print(e);
print(typeof(e));
print(left(e));
print(typeof(left(e)));
print(right(e));
print(typeof(right(e)));

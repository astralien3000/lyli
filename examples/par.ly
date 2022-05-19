"a" * 5 + 3;
"a" + 5 * 3;
"a" + (5 * 3);
"a" + ((5 . 3));
("a" + 5) * 3;
(("a" + 5)) * 3;
"a" ! ((5 & 54) & 2);
op("a")(2,3);
op(+)(2,3);

fn op(+)(a, b) {
  return a + b;
};

op(*)(4,4) + op(/)(2,2);

0 + 0;
(0 + 0);
(0) + (0);
((0) + (0));

let a = 0 + 0;
let a = (0 + 0);

f(0);

++a;
a++;

(++a) * 3;

return (a++);
return (*a);
return a + 5;

(a + 2) . in [5, 8, 8, 9];
a << b;
op(<<) << a & b;
return (-a);
return (+"lool");
return (5++);

for (a in list(5,8,7)) {};
5 + (a and b) * 3;

let a = fn(a, b) { a + b } ();
let b : int = 0 + 1;

/// comment
a ! /*comment*/ b;

a !!:.? b;
a ==== b;
a <==> b;
a - (b++);
a - (-b);
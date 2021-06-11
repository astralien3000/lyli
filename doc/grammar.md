# Grammar

## A lisp language...

Lisp looks like (example of naive recursive fibonacci function) :

```lisp
(defun fib (n)
  (if (< n 2) n
      (+ (fib (- n 1)) (fib (- n 2)))))
```

The main feature of lisp grammar is : everything is a list.
Lyli can be considered as quite similar : in Lyli, everything is a Call.

A call in Lyli can have these forms : 

```
function ( argument1 , argument 2 , ... );

function ( argument1 ; argument 2 ; ... );

function [ argument1 , argument 2 , ... ];

function [ argument1 ; argument 2 ; ... ];

function { argument1 , argument 2 , ... };

function { argument1 ; argument 2 ; ... };
```

All these lines are strictly equivalent and have the same behavior.

A straight forward translation of the previous lisp code could be :

```
defun(fib, n(),
  if(<(n, 2), n, 
     +(fib(-(n, 1)), fib(-(n, 2)))))
```

This is gramatically valid in Lyli while not being valid with only the basic Lyli prelude.

But this still look like lisp, next part will explain a feature that enable Lyli to look like a more mainstream language like C.

## ...that can look like an other language

### Let's look at an example

Le'ts take a look at the same example, written in C :

```c
int fib(int n) {
  if(n < 2) {
    return n;
  }
  else {
    return fib(n-1) + fib(n-2);
  }
}
```

In the C language, and most mainstream languages, statements like function declaration, control flow structures, and mathematical expressions are described by the grammar.

```c
// Function definition
int fib(...) { ... }
```

```c
// Parameter / Variable declaration
int n
```

```c
// if/else control structure
  if(...) { ... } else { ... }
```

```c
// mathematical expression
n < 2
n-1
n-2
fib(n-1) + fib(n-2)
```

```c
// Return statement
return n;
return fib(n-1) + fib(n-2);
```

What is the common form of those statements ?

They are just sequence of Call/Atomic expressions... separeted by space !

### Space is the real operator !

So let's define a statement in Lyli as a sequence of expressions separated by spaces : 

```
expr expr ...
```

But we placed ourself in the lisp world, we need to attach this to a Lyli expression, hence a Call.

The space is actually the only operator recognised by the grammar, it is symbolised by an underscore `_`.

```
_(expr, expr, ...)
```

As any Call expression, and at the contrary of some others language, statements in Lyli can always return a value (if wanted), even a function definition for example.

### Final form

```
fn fib(n) {
  if(n < 2) {
    n
  }
  else {
    fib(n-1) + fib(n-2)
  }
};
```

 - Functions will return their last statement (hence no `;` after the else)
 - if/else statements also return the last statement of their respective branch.

This is equivalent to :

```
_(fn, fib(n) (
  _(if(_(n, <, 2)) (
    n
  ),
  else (
    _(fib(_(n,-,1)), +, fib(_(n,-,2)))
  ))
)),
```

## The problem of parenthesis in mathematical operations

### Weird expression tree

The choices made for the grammar made much more difficult the use of parenthesis in mathematical expressions.

```
2 * (1 + 1)
```

Would look like :

```
_(2, *(_(1, +, 1)))
```

Indeed, a parenthesis will be associated to the previous expression, to make a Call expression.

Which is more complex than what we could expect : 

```
_(2, *, _(1, +, 1))
```

The parenthesis need to be following a symbol, for example : 

```
2 * _(1 + 1)
```

This is actually equivalent to : 

```
_(2, *, _(_(1, +, 1)))
```

But the nested `_` is not a problem since the "upper" `_` will do nothing to the expression.

### Impossible synthax

Even worse, if the parenthesis is at the beginning of the statement, this is not gramatically valid : 

```
(1 + 1) * 2;  // PARSING ERROR !!
```

Of course this can be resolved by the previous trick :

```
_(1 + 1) * 2;  // Ok
```

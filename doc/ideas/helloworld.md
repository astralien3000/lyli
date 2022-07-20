# Hello, World !

## REPL

Lyli can run as a Read-Eval-Print-Loop :

```sh
$ lyli
```

and write in the prompt :

```
> print("Hello, world!")
Hello, world!
```

## Interpreter

Create a file named hello.ly :

```
print("Hello, world!")
```

Compile and run it : 

```sh
$ lyli hello.ly
Hello, world!
```

## Compiler

Create a file named main.ly :

```
fn main() {
  print("Hello, world!")
}
```

Compile and run it : 

```sh
$ lyli main.ly
$ ./main
Hello, world!
```

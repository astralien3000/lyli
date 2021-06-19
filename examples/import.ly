import lark;

let a = Lark(""" 
start : "a" "+" "b" 
""");
int b = Lark("start : ");

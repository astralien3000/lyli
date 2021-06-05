import lark;

var a = Lark(""" 
start : "a" "+" "b" 
""");
int b = Lark("start : ");


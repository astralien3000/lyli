import lark;

let a = Lark(""" 
start : "a" "+" "b" 
""");
let b = Lark("start : ");

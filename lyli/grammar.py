grammar = """start : instr_list

instr : expr
      | stmt

expr : atomic_expr
     | call_expr

stmt : expr (expr)+

atomic_expr : string_expr
            | integer_expr
            | symbol_expr
            | operator

call_expr : expr "(" instr_list ")"
          | expr "{" instr_list "}"
          | expr "[" instr_list "]"

instr_list : (instr ",")* instr?
           | (instr ";")* instr?

operator : PP | MM
         | DOT | ARROW
         | MUL | BWAND | NOT | BWNOT
         | DIV | MOD
         | ADD | SUB
         | LT | GT | LE | GE
         | EQ | NEQ
         | OR
         | ASSIGN
         | EVAL
         | SCOPE

SCOPE : "::"

EVAL : "$"

PP : "++"
MM : "--"

DOT : "."
ARROW : "->"

MUL : "*"
BWAND : "&"
NOT : "!"
BWNOT : "~"

DIV : "/"
MOD : "%"

ADD : "+"
SUB : "-"

LT : "<"
GT : ">"
LE : "<="
GE : ">="

EQ : "=="
NEQ : "!="

OR : "||"

ASSIGN : "="

string_expr : STRING | longstring_expr
longstring_expr : LONGSTRING

integer_expr : CONSTANTI

symbol_expr : IDENTIFIER

STRING : /\"[^\"\\n]*\"/
LONGSTRING : /\"\"\"([^\"]|\"\"?[^\"])+\"\"\"/
IDENTIFIER : /[^\W\d]\w*/
CONSTANTI : /\d+\w*/
CONSTANTF : /\d+\.\d*\w*/

WS : /\s/
%ignore WS
"""
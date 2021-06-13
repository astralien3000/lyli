grammar = """start : instr_list

instr : expr
      | stmt

expr : atomic_expr
     | call_expr

stmt : expr (expr)+

atomic_expr : string_expr
            | longstring_expr
            | float_expr
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

string_expr : STRING
longstring_expr : LONGSTRING

integer_expr : INT_LITERAL
             | BIN_LITERAL
             | OCT_LITERAL
             | DEC_LITERAL
             | HEX_LITERAL
             | ZERO_LITERAL

float_expr : FLOAT_LITERAL

symbol_expr : IDENTIFIER

INT_LITERAL : /[1-9]([0-9]|_[0-9])*/
BIN_LITERAL : /0b[01]([01]|_[01])*/
OCT_LITERAL : /0o[0-7]([0-7]|_[0-7])*/
DEC_LITERAL : /0d[0-9]([0-9]|_[0-9])*/
HEX_LITERAL : /0x[0-9a-fA-F]([0-9a-fA-F]|_[0-9a-fA-F])*/
ZERO_LITERAL : /0/

FLOAT_LITERAL : FLOAT_INTEGER (FLOAT_DECIMAL|FLOAT_EXPONENT|FLOAT_DECIMAL FLOAT_EXPONENT)
FLOAT_INTEGER : /(0|[1-9]([0-9]|_[0-9])*)/
FLOAT_DECIMAL : /\.[0-9]([0-9]|_[0-9])*/
FLOAT_EXPONENT : /[eE][0-9]([0-9]|_[0-9])*/

STRING : /\"[^\"\\n]*\"/
LONGSTRING : /\"\"\"([^\"]|\"\"?[^\"])+\"\"\"/

IDENTIFIER : /[^\W\d]\w*/

COMMENT : "//" /[^\\n]*/
LONGCOMMENT : "/*" /.*/ "*/"

WS : /\s/
%ignore WS
%ignore COMMENT
%ignore LONGCOMMENT
"""
grammar = """start : instr_list

instr : expr
      | stmt

expr : atomic_expr
     | call_expr
     | uop_expr
     | bop_expr
     | "(" expr ")"

stmt : expr (expr)+

atomic_expr : string_expr
            | longstring_expr
            | char_expr
            | float_expr
            | integer_expr
            | symbol_expr
            | operator

call_expr: expr ("!")? "(" instr_list ")"
         | expr "{" instr_list "}"
         | expr "[" instr_list "]"
         | expr "<" instr_list ">"

bop_expr: expr operator expr

uop_expr: uop_prefix_expr
        | uop_suffix_expr

uop_prefix_expr: pre_uop expr
uop_suffix_expr: expr suf_uop

instr_list: (instr ",")* instr?
          | (instr ";")* instr?

pre_uop: PP | MM
       | EVAL
       | NOT | BWNOT
       | MUL | BWAND

suf_uop: PP | MM

cmpd_op: ARROW
       | LSHIFT | RSHIFT
       | AND | OR
       | POW
       | LSHIFT | RSHIFT
       | SCOPE
       | IAND | IOR
       | IMUL
       | IBWAND | IBWOR
       | INOT | IBWNOT
       | IDIV | IMOD
       | IADD | ISUB
       | LE | GE
       | EQ | NEQ

smpl_op: DOT
       | MUL
       | BWAND | BWOR 
       | DIV | MOD
       | ADD | SUB
       | LT | GT
       | ASSIGN
       | COLON

operator: cmpd_op | smpl_op

COLON : ":"

SCOPE : "::"

EVAL : "$"

PP : "++"
MM : "--"

DOT : "."
ARROW : "->"

AND : "&&"
OR : "||"

MUL : "*"
POW : "**"
BWAND : "&"
BWOR : "|"
NOT : "!"
BWNOT : "~"

DIV : "/"
MOD : "%"

ADD : "+"
SUB : "-"

LSHIFT : "<<"
RSHIFT : ">>"

LT : "<"
GT : ">"
LE : "<="
GE : ">="

EQ : "=="
NEQ : "!="

ASSIGN : "="

IAND : "&&="
IOR : "||="

IMUL : "*="
IBWAND : "&="
IBWOR : "|="
INOT : "!="
IBWNOT : "~="

IDIV : "/="
IMOD : "%="

IADD : "+="
ISUB : "-="

ILSHIFT : "<<="
IRSHIFT : ">>="

string_expr : STRING

longstring_expr : LONGSTRING

char_expr : CHAR_LITERAL

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

FLOAT_LITERAL : FLOAT_INTEGER FLOAT_DECIMAL FLOAT_EXPONENT
              | FLOAT_INTEGER FLOAT_DECIMAL
              | FLOAT_INTEGER FLOAT_EXPONENT

FLOAT_INTEGER : /(0|[1-9]([0-9]|_[0-9])*)/
FLOAT_DECIMAL : /\.[0-9]([0-9]|_[0-9])*/
FLOAT_EXPONENT : /[eE][0-9]([0-9]|_[0-9])*/

STRING : /\"[^\"\\n]*\"/
LONGSTRING : /\"\"\"([^\"]|\"\"?[^\"])+\"\"\"/
CHAR_LITERAL : /'[^'\\n]'/

IDENTIFIER : /[^\W\d]\w*/

COMMENT : ("//"|"#") /[^\\n]*/
LONGCOMMENT : "/*" /.*/ "*/"

WS : /\s/
%ignore WS
%ignore COMMENT
%ignore LONGCOMMENT
"""
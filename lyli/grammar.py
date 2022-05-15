grammar = """start : instr_list

instr : expr
      | stmt
      | bop_stmt
      | uop_expr
      | operator
      | "(" instr ")"

expr : atomic_expr
     | call_expr

stmt : expr (expr)+
     | expr (expr)* bop_expr

atomic_expr : string_expr
            | longstring_expr
            | char_expr
            | float_expr
            | integer_expr
            | symbol_expr

call_expr: expr ("!")? "(" instr_list ")"
         | expr "{" instr_list "}"
         | expr "[" instr_list "]"

par_expr: expr | "(" instr ")"

bop_expr: expr (all_bop par_expr)+
bop_stmt: par_expr (all_bop par_expr)+

uop_expr: uop_prefix_expr
        | uop_suffix_expr

uop_prefix_expr: pre_uop expr
uop_suffix_expr: expr suf_uop

instr_list: (instr ",")* instr?
          | (instr ";")* instr?

puop: EVAL
    | NOT | BWNOT
    | AT

buop: SUB | ADD
    | MUL | BWAND

suf_uop: PP | MM

cmpd_bop: LARROW | RARROW
        | BIGRARROW
        | LSHIFT | RSHIFT
        | LLSHIFT | RRSHIFT
        | AND | OR
        | POW
        | LSHIFT | RSHIFT
        | SCOPE
        | IAND | IOR
        | IMUL | IPOW
        | IBWAND | IBWOR | IBWXOR
        | INOT | IBWNOT
        | IDIV | IMOD
        | IADD | ISUB
        | LE | GE
        | EQ | NE
        | EEQ | NEE

par_bop: LT | GT

smpl_bop: DOT
        | BWOR | BWXOR
        | DIV | MOD
        | ASSIGN
        | COLON

pre_uop: buop | puop | suf_uop

all_bop: cmpd_bop | smpl_bop | par_bop | buop

operator: all_bop | puop | suf_uop

COLON : ":"

SCOPE : "::"

EVAL : "$"

AT : "@"

PP : "++"
MM : "--"

DOT : "."

LARROW : "<-"
RARROW : "->"

BIGRARROW : "=>"

AND : "&&"
OR : "||"

MUL : "*"
POW : "**"

BWAND : "&"
BWOR : "|"
BWXOR : "^"

NOT : "!"
BWNOT : "~"

DIV : "/"
MOD : "%"

ADD : "+"
SUB : "-"

LSHIFT : "<<"
RSHIFT : ">>"

LLSHIFT : "<<<"
RRSHIFT : ">>>"

LT : "<"
GT : ">"
LE : "<="
GE : ">="

EQ : "=="
NE : "!="

EEQ : "==="
NEE : "!=="

ASSIGN : "="

IAND : "&&="
IOR : "||="

IMUL : "*="
IPOW : "**="

IBWAND : "&="
IBWOR : "|="
IBWXOR : "^="

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
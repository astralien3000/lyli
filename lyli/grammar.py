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

integer_expr : DEC_LITERAL
             | BIN_LITERAL
             | HEX_LITERAL
             | OCT_LITERAL

symbol_expr : IDENTIFIER

DEC_LITERAL : /0|[1-9][0-9_]*/ INTEGER_SUFFIX?
BIN_LITERAL : /0b[01]([01]|_[01])*/ INTEGER_SUFFIX?
HEX_LITERAL : /0x[0-9a-fA-F]([0-9a-fA-F]|_[0-9a-fA-F])*/ INTEGER_SUFFIX?
OCT_LITERAL : /0o[0-7]([0-7]|_[0-7])*/ INTEGER_SUFFIX?

INTEGER_SUFFIX : "u8"|"u16"|"u32"|"u64"
               | "i8"|"i16"|"i32"|"i64"

STRING : /\"[^\"\\n]*\"/
LONGSTRING : /\"\"\"([^\"]|\"\"?[^\"])+\"\"\"/
IDENTIFIER : /[^\W\d]\w*/
CONSTANTF : /\d+\.\d*\w*/

COMMENT : "//" /[^\\n]*/
LONGCOMMENT : "/*" /.*/ "*/"

WS : /\s/
%ignore WS
%ignore COMMENT
%ignore LONGCOMMENT
"""
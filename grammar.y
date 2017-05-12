%{
#include "ast.hpp"

extern "C"
{

extern int yylineno;
int yylex ();
int yyerror (const char* s);

}

%}

%union { float fval; long ival; char str[1024]; void* any; }

%token <str>IDENTIFIER
%token <str>STRING
%token <fval>CONSTANTF <ival>CONSTANTI 
%token INC_OP DEC_OP LE_OP GE_OP EQ_OP NE_OP
%token SUB_ASSIGN MUL_ASSIGN ADD_ASSIGN
%token TYPE_NAME
%token INT FLOAT VOID

%start global
%%

global
: instruction_list
;

instruction_list
: instruction ';' instruction_list
| instruction
|
;

instruction
: def_instruction
| ret_instruction
;

def_instruction
: var_def
| func_def
;

ret_instruction
: val_instruction
| ref_instruction
;

val_instruction
: string_constant
| integer_constant
| instr_block
| tuple
;

ref_instruction
: call
| symbol
| dot_expr
;

integer_constant
: CONSTANTI
;

string_constant
: STRING
;

var_decl
: ref_instruction IDENTIFIER
;

var_def
: var_decl
| var_decl '=' ret_instruction
;

func_decl
: ref_instruction ref_instruction IDENTIFIER params_list
;

func_def
: func_decl
| func_decl '=' ret_instruction
;

instr_block
: instr_block_begin instruction_list instr_block_end
;

instr_block_begin
: '{'
;

instr_block_end
: '}'
;

params_list
: params_list_begin param_list params_list_end
| params_list_begin params_list_end
;

params_list_begin
: '('
;

params_list_end
: ')'
;

param_list
: param_list_element ',' params_list
| param_list_element
;

param_list_element
: var_def
;

tuple
: tuple_begin value_list tuple_end
;

tuple_begin
: '('
;

tuple_end
: ')'
;

value_list
: value_list_element ',' value_list
| value_list_element
|
;

value_list_element
: ret_instruction
;

call
: ref_instruction tuple
| ref_instruction instr_block
;

symbol
: IDENTIFIER
;

dot_expr
: ref_instruction '.' symbol
;

%%
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

extern int column;
extern int yylineno;
extern FILE *yyin;

char *file_name = NULL;

int yyerror (const char *s) {
  fflush (stdout);
  fprintf (stderr, "%s:%d:%d: %s\n", file_name, yylineno, column, s);
  return 0;
}

int main (int argc, char *argv[]) {
  FILE *input = NULL;
  if (argc==2) {
    input = fopen (argv[1], "r");
    file_name = strdup (argv[1]);
    if (input) {
      yyin = input;
    }
    else {
      fprintf (stderr, "%s: Could not open %s\n", *argv, argv[1]);
      return 1;
    }
  }
  else {
    fprintf (stderr, "%s: error: no input file\n", *argv);
    return 1;
  }

  yyparse ();

  free (file_name);
  return 0;
}

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
: instr_list
;

instr_list
: instr ';' instr_list
| instr
|
;

instr
: def_instr
| ret_instr
;

def_instr
: var_def_instr
| func_def_instr
;

ret_instr
: val_instr
| ref_instr
;

val_instr
: string_instr
| integer_instr
| instr_tuple_instr
| value_tuple_instr
;

ref_instr
: call_instr
| symbol_instr
| dot_expr_instr
;

string_instr
: STRING
;

integer_instr
: CONSTANTI
;

var_decl
: ref_instr IDENTIFIER
;

var_def_instr
: var_decl
| var_decl '=' ret_instr
;

func_decl
: ref_instr ref_instr IDENTIFIER params_tuple
;

func_def_instr
: func_decl
| func_decl '=' ret_instr
;

instr_tuple_instr
: instr_block_begin instr_list instr_block_end
;

instr_block_begin
: '{'
;

instr_block_end
: '}'
;

params_tuple
: params_tuple_begin param_list params_tuple_end
| params_tuple_begin params_tuple_end
;

params_tuple_begin
: '('
;

params_tuple_end
: ')'
;

param_list
: param_list_element ',' params_tuple
| param_list_element
;

param_list_element
: var_def_instr
;

value_tuple_instr
: value_tuple_begin value_list value_tuple_end
;

value_tuple_begin
: '('
;

value_tuple_end
: ')'
;

value_list
: value_list_element ',' value_list
| value_list_element
|
;

value_list_element
: ret_instr
;

call_instr
: ref_instr value_tuple_instr
| ref_instr instr_tuple_instr
;

symbol_instr
: IDENTIFIER
;

dot_expr_instr
: ref_instr '.' symbol_instr
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

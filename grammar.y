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

%type <any> instruction_list
%type <any> instruction_list_element

%type <any> instruction
%type <any> def_instruction
%type <any> val_instruction

%type <any> template_tuple
%type <any> template_list
%type <any> template_list_element

%type <any> symbol
%type <any> symbol_expr

%type <any> integer_constant
%type <any> string_constant

%type <any> call

%type <any> tuple

%type <any> instr_block

%type <any> var_decl
%type <any> var_def

%type <any> func_decl
%type <any> func_def

%type <any> value_list
%type <any> value_list_element

%type <any> params_def
%type <any> param_list
%type <any> param_def

%start global
%%

global
: instruction_list
{
  InstrBlock* list = (InstrBlock*)$1;
  if(list != NULL) {
    cout << list->size() << endl;
    for(auto it = list->rbegin() ; it != list->rend() ; it++) {
      cout << (*it)->str() << ";" << endl;
    }
  }
}
;

instruction_list
: instruction_list_element instruction_list
{
  Instruction* elem = (Instruction*)$1;
  InstrBlock* list = (InstrBlock*)$2;
  if(elem != NULL) {
    list->push_back(elem);
  }
  $$ = $2;
}
|
{
  $$ = (void*)new InstrBlock();
}
;

instruction_list_element
: instruction ';'
{
  $$ = $1;
}
;

instruction
: def_instruction
{
  $$ = $1;
}
| val_instruction
{
  $$ = $1;
}
|
{
  $$ = NULL;
}
;

def_instruction
: var_def
{
  $$ = $1;
}
| func_def
{
  $$ = $1;
}
;

val_instruction
: symbol_expr
{
  $$ = $1;
}
| string_constant
{
  $$ = $1;
}
| integer_constant
{
  $$ = $1;
}
| instr_block
{
  $$ = $1;
}
| tuple
{
  $$ = $1;
}
| call
{
  $$ = $1;
}
;

integer_constant
: CONSTANTI
{
  auto ret = new IntegerConstantInstruction();
  ret->value = $1;
  $$ = (void*)ret;
}
;

string_constant
: STRING
{
  auto ret = new StringInstruction();
  ret->value = $1;
  $$ = (void*)ret;
}
;

var_decl
: symbol_expr IDENTIFIER
{
  auto ret = new VarDecl();
  ret->name = $2;
  ret->type = (SymbolExpr*)$1;
  $$ = (void*)ret;
}
;

var_def
: var_decl
{
  auto ret = new DefInstruction();
  ret->decl = (VarDecl*)$1;
  ret->value = NULL;
  $$ = (void*)ret;
}
| var_decl '=' val_instruction
{
  auto ret = new DefInstruction();
  ret->decl = (VarDecl*)$1;
  ret->value = (ValInstruction*)$3;
  $$ = (void*)ret;
}
;

func_decl
: symbol_expr symbol_expr IDENTIFIER params_def
{
  auto base_type = (SymbolExpr*)$1;
  auto func_return_type = (SymbolExpr*)$2;
  auto func_params = (Params*)$4;
  auto func_type = new Call();
  func_type->symbol = func_return_type;
  func_type->tuple = func_params->typeTuple();
  func_type->block = NULL;
  if(base_type->last()->tlist == NULL) {
    base_type->last()->tlist = new TemplateList();
  }
  base_type->last()->tlist->insert(base_type->last()->tlist->begin(), func_type);
  auto ret = new VarDecl();
  ret->name = $3;
  ret->type = base_type;
  $$ = (void*)ret;
}
| symbol_expr IDENTIFIER params_def
{
  auto base_type = (SymbolExpr*)$1;
  auto func_return_type = new Symbol();
  func_return_type->name = "void";
  func_return_type->tlist = NULL;
  auto func_params = (Params*)$3;
  auto func_type = new Call();
  func_type->symbol = func_return_type;
  func_type->tuple = func_params->typeTuple();
  func_type->block = NULL;
  if(base_type->last()->tlist == NULL) {
    base_type->last()->tlist = new TemplateList();
  }
  base_type->last()->tlist->insert(base_type->last()->tlist->begin(), func_type);
  auto ret = new VarDecl();
  ret->name = $2;
  ret->type = base_type;
  $$ = (void*)ret;
}
;

func_def
: func_decl
{
  auto ret = new DefInstruction();
  ret->decl = (VarDecl*)$1;
  ret->value = NULL;
  $$ = (void*)ret;
}
| func_decl '=' instr_block
{
  auto ret = new DefInstruction();
  ret->decl = (VarDecl*)$1;
  ret->value = (ValInstruction*)$3;
  $$ = (void*)ret;
}
;

instr_block
: instr_block_begin instruction_list instr_block_end
{
  $$ = $2;
}
;

instr_block_begin
: '{'
;

instr_block_end
: '}'
;

tuple
: tuple_begin value_list tuple_end
{
  $$ = $2;
}
;

tuple_begin
: '('
;

tuple_end
: ')'
;

value_list
: value_list_element ',' value_list
{
  auto ret = (Tuple*)$3;
  auto elem = (ValInstruction*)$1;
  if(elem != NULL) {
    ret->push_back(elem);
  }
  $$ = $3;
}
| value_list_element
{
  auto ret = new Tuple();
  ret->push_back((ValInstruction*)$1);
  $$ = (void*)ret;
}
|
{
  $$ = (void*)new Tuple();
}
;

value_list_element
: val_instruction
{
  $$ = $1;
}
;

params_def
: tuple_begin param_list tuple_end
{
  $$ = $2;
}
;

param_list
: param_def ',' param_list
{
  auto ret = (Params*)$1;
  ret->push_back((DefInstruction*)$3);
  $$ = (void*)ret;
}
| param_def
{
  auto ret = new Params();
  ret->push_back((DefInstruction*)$1);
  $$ = (void*)ret;
}
;

param_def
: var_def
{
  $$ = $1;
}
;

call
: symbol_expr tuple
{
  auto ret = new Call();
  ret->symbol = (SymbolExpr*)$1;
  ret->tuple = (Tuple*)$2;
  ret->block = NULL;
  $$ = (void*)ret;
}
| symbol_expr       instr_block
{
  auto ret = new Call();
  ret->symbol = (SymbolExpr*)$1;
  ret->tuple = NULL;
  ret->block = (InstrBlock*)$2;
  $$ = (void*)ret;
}
| symbol_expr tuple instr_block
{
  auto ret = new Call();
  ret->symbol = (SymbolExpr*)$1;
  ret->tuple = (Tuple*)$2;
  ret->block = (InstrBlock*)$3;
  $$ = (void*)ret;
}
;

symbol_expr
: symbol '.' symbol_expr
{
  auto ret = new DotSymbolExpr();
  ret->first = (Symbol*)$1;
  ret->second = (SymbolExpr*)$3;
  $$ = (void*)ret;
}
| symbol
{
  $$ = $1;
}
;

symbol
: IDENTIFIER
{
  auto ret = new Symbol();
  ret->name = $1;
  ret->tlist = NULL;
  $$ = (void*)ret;
}
| IDENTIFIER template_tuple
{
  auto ret = new Symbol();
  ret->name = $1;
  ret->tlist = (TemplateList*)$2;
  $$ = (void*)ret;
}
;

template_tuple
: '<' template_list '>'
{
  $$ = $2;
}
;

template_list
: template_list_element ',' template_list
{
  auto elem = (ValInstruction*)$1;
  auto ret = (TemplateList*)$3;
  if(elem != NULL) {
    ret->push_back(elem);
  }
  $$ = $3;
}
| template_list_element
{
  auto elem = (ValInstruction*)$1;
  auto ret = new TemplateList();
  if(elem != NULL) {
    ret->push_back(elem);
  }
  $$ = (void*)ret;
}
;

template_list_element
: val_instruction
{
  $$ = $1;
}
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

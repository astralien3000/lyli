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
: instruction_list_element ';' instruction_list
{
  auto elem = (Instruction*)$1;
  auto list = (InstrBlock*)$3;
  if(elem != NULL) {
    list->push_back(elem);
  }
  $$ = $3;
}
| instruction_list_element
{
  auto list = new InstrBlock();
  auto elem = (Instruction*)$1;
  if(elem != NULL) {
    list->push_back(elem);
  }
  $$ = (void*)list;
}
|
{
  $$ = (void*)new InstrBlock();
}
;

instruction_list_element
: instruction
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
  auto ret = new Call();
  auto decl = (VarDecl*)$1;
  
  auto symbol = new Symbol();
  symbol->name = "define";
  symbol->tlist = new TemplateList();
  symbol->tlist->push_back(decl->type);
  ret->symbol = symbol;
  
  ret->tuple = new Tuple();
  ret->tuple->push_back(decl->symbolInstr());
  
  $$ = (void*)ret;
}
| var_decl '=' val_instruction
{
  auto ret = new Call();
  auto decl = (VarDecl*)$1;
  auto instr = (ValInstruction*)$3;
  
  auto symbol = new Symbol();
  symbol->name = "define";
  symbol->tlist = new TemplateList();
  symbol->tlist->push_back(decl->type);
  ret->symbol = symbol;
  
  ret->tuple = new Tuple();
  ret->tuple->push_back(instr);
  ret->tuple->push_back(decl->symbolInstr());

  $$ = (void*)ret;
}
;

func_decl
: symbol_expr symbol_expr IDENTIFIER params_def
{
  auto ret = new FuncDecl();
  ret->name = $3;
  ret->type = (SymbolExpr*)$1;
  ret->return_type = (SymbolExpr*)$2;
  ret->params = (InstrBlock*)$4;
  $$ = (void*)ret;
}
| symbol_expr IDENTIFIER params_def
{
  auto ret = new FuncDecl();
  ret->name = $2;
  ret->type = (SymbolExpr*)$1;
  ret->return_type = NULL;
  ret->params = (InstrBlock*)$3;
  $$ = (void*)ret;
}
;

func_def
: func_decl
{
  auto ret = new Call();
  auto decl = (FuncDecl*)$1;
  
  auto symbol = new Symbol();
  symbol->name = "define";
  symbol->tlist = new TemplateList();
  symbol->tlist->push_back(decl->type);
  ret->symbol = symbol;
  
  ret->tuple = new Tuple();
  ret->tuple->push_back(decl->params);

  auto rtype = new InstrBlock();
  ret->tuple->push_back(rtype);
  if(decl->return_type != NULL) { 
    rtype->push_back(decl->return_type);
  }
  ret->tuple->push_back(decl->symbolInstr());

  $$ = (void*)ret;
}
| func_decl '=' instr_block
{
  auto ret = new Call();
  auto decl = (FuncDecl*)$1;
  auto instr = (ValInstruction*)$3;
  
  auto symbol = new Symbol();
  symbol->name = "define";
  symbol->tlist = new TemplateList();
  symbol->tlist->push_back(decl->type);
  ret->symbol = symbol;
  
  ret->tuple = new Tuple();
  ret->tuple->push_back(instr);
  ret->tuple->push_back(decl->params);
  auto rtype = new InstrBlock();
  ret->tuple->push_back(rtype);
  if(decl->return_type != NULL) { 
    rtype->push_back(decl->return_type);
  }
  ret->tuple->push_back(decl->symbolInstr());

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
  auto ret = (InstrBlock*)$1;
  ret->push_back((Instruction*)$3);
  $$ = (void*)ret;
}
| param_def
{
  auto ret = new InstrBlock();
  ret->push_back((Instruction*)$1);
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
  $$ = (void*)ret;
}
| symbol_expr       instr_block
{
  auto ret = new Call();
  ret->symbol = (SymbolExpr*)$1;
  ret->tuple = new Tuple();
  ret->tuple->push_back((InstrBlock*)$2);
  $$ = (void*)ret;
}
| symbol_expr tuple instr_block
{
  auto ret = new Call();
  ret->symbol = (SymbolExpr*)$1;
  ret->tuple = (Tuple*)$2;
  ret->tuple->insert(ret->tuple->begin(), (InstrBlock*)$3);
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

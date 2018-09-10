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

%type<any> string_instr val_instr symbol_instr ret_instr value_list_element value_list ref_instr value_tuple_instr
%type<any> call_instr instr instr_list instr_tuple_instr global func_decl def_instr func_def_instr dot_expr_instr
%type<any> integer_instr var_decl var_def_instr

%start global
%%

global
: instr_list {
	Global* ret = new Global();
	ret->instrs = (list<Instr*>*)$1;
	cout << ret->str() << endl;
	$$ = ret;
}
;

instr_list
: instr ';' instr_list {
	list<Instr*>* ret = (list<Instr*>*)$3;
	ret->push_front((Instr*)$1);
	$$ = ret;
}
| instr {
	list<Instr*>* ret = new list<Instr*>();
	ret->push_front((Instr*)$1);
	$$ = ret;
}
| {
	list<Instr*>* ret = new list<Instr*>();
	$$ = ret;
}
;

instr
: def_instr {
	$$ = $1;
}
| ret_instr {
	$$ = $1;
}
;

def_instr
: var_def_instr {
	$$ = $1;
}
| func_def_instr {
	$$ = $1;
}
;

ret_instr
: val_instr {
	$$ = $1;
}
| ref_instr {
	$$ = $1;
}
;

val_instr
: string_instr {
	$$ = $1;
}
| integer_instr {
	$$ = $1;
}
| instr_tuple_instr {
	$$ = $1;
}
| value_tuple_instr {
	$$ = new Unsupported();
}
;

ref_instr
: call_instr {
	$$ = $1;
}
| symbol_instr {
	$$ = $1;
}
| dot_expr_instr {
	$$ = $1;
}
;

string_instr
: STRING {
	StringInstr* ret = new StringInstr();
	ret->value = $1;
	$$ = ret;
}
;

integer_instr
: CONSTANTI {
	IntegerInstr* ret = new IntegerInstr();
	ret->value = $1;
	$$ = ret;
}
;

var_decl
: ref_instr IDENTIFIER {
	RefInstr* var_type = (RefInstr*)$1;

	SymbolInstr* var_sym = new SymbolInstr();
	var_sym->name = $2;
		
	SymbolInstr* def = new SymbolInstr();
	def->name = "define";
	
	CallInstr* ret = new CallInstr();
	ret->ref = def;
	ret->params = new ValueTupleInstr();
	ret->params->instrs = new list<RetInstr*>();
	ret->params->instrs->push_back(var_type);
	ret->params->instrs->push_back(var_sym);
	
	$$ = ret;
}
;

var_def_instr
: var_decl {
	$$ = $1;
}
| var_decl '=' ret_instr {
	CallInstr* ret = (CallInstr*)$1;
	ret->params->instrs->push_back((RetInstr*)$3);
	$$ = ret;
}
;

func_decl
: ref_instr ref_instr IDENTIFIER params_tuple {
	RefInstr* func_type = (RefInstr*)$1;
	RefInstr* ret_type = (RefInstr*)$2;

	SymbolInstr* func_sym = new SymbolInstr();
	func_sym->name = $3;
	
	InstrTupleInstr* params = new InstrTupleInstr();
	params->instrs = new list<Instr*>();
	
	SymbolInstr* def = new SymbolInstr();
	def->name = "defun";
	
	CallInstr* ret = new CallInstr();
	ret->ref = def;
	ret->params = new ValueTupleInstr();
	ret->params->instrs = new list<RetInstr*>();
	ret->params->instrs->push_back(func_type);
	ret->params->instrs->push_back(func_sym);
	ret->params->instrs->push_back(params);
	ret->params->instrs->push_back(ret_type);
	
	$$ = ret;
}
;

func_def_instr
: func_decl {
	$$ = $1;
}
| func_decl '=' ret_instr {
	CallInstr* ret = (CallInstr*)$1;
	ret->params->instrs->push_back((RetInstr*)$3);
	$$ = ret;
}
;

instr_tuple_instr
: instr_block_begin instr_list instr_block_end {
	InstrTupleInstr* ret = new InstrTupleInstr();
	ret->instrs = (list<Instr*>*)$2;
	$$ = ret;
}
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
: value_tuple_begin value_list value_tuple_end {
	ValueTupleInstr* ret = new ValueTupleInstr();
	ret->instrs = (list<RetInstr*>*)$2;
	$$ = ret;
}
;

value_tuple_begin
: '('
;

value_tuple_end
: ')'
;

value_list
: value_list_element ',' value_list {
	list<RetInstr*>* ret = (list<RetInstr*>*)$3;
	ret->push_front((RetInstr*)$1);
	$$ = ret;
}
| value_list_element {
	list<RetInstr*>* ret = new list<RetInstr*>();
	ret->push_front((RetInstr*)$1);
	$$ = ret;
}
| {
	list<RetInstr*>* ret = new list<RetInstr*>();
	$$ = ret;
}
;

value_list_element
: ret_instr {
	$$ = $1;
}
;

call_instr
: ref_instr value_tuple_instr {
	CallInstr* ret = new CallInstr();
	ret->ref = (RefInstr*)$1;
	ret->params = (ValueTupleInstr*)$2;
	$$ = ret;
}
| ref_instr instr_tuple_instr {
	CallInstr* ret = new CallInstr();
	ret->ref = (RefInstr*)$1;
	ret->params = new ValueTupleInstr();
	ret->params->instrs = new list<RetInstr*>();
	ret->params->instrs->push_front((RetInstr*)$2);
	$$ = ret;
}
;

symbol_instr
: IDENTIFIER {
	SymbolInstr* ret = new SymbolInstr();
	ret->name = $1;
	$$ = ret;
}
;

dot_expr_instr
: ref_instr '.' symbol_instr {
	RetInstr* left = (RetInstr*)$1;

	InstrTupleInstr* right = new InstrTupleInstr();
	right->instrs = new list<Instr*>();
	right->instrs->push_back((Instr*)$3);

	SymbolInstr* def = new SymbolInstr();
	def->name = "__op_dot__";
	
	CallInstr* ret = new CallInstr();
	ret->ref = def;
	ret->params = new ValueTupleInstr();
	ret->params->instrs = new list<RetInstr*>();
	ret->params->instrs->push_back(left);
	ret->params->instrs->push_back(right);
	
	$$ = ret;
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

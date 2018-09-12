%{
#include "ast.hpp"
#include "ctx.hpp"

extern "C"
{

extern int yylineno;
int yylex ();
int yyerror (const char* s);

}

Global* global;

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
%type<any> integer_instr var_decl var_def_instr param_list_element param_list params_tuple

%start global
%%

global
: instr_list {
	global = new Global();
	global->instrs = (list<RetInstr*>*)$1;
	$$ = global;
}
;

instr_list
: instr ';' instr_list {
	list<RetInstr*>* ret = (list<RetInstr*>*)$3;
	ret->push_front((RetInstr*)$1);
	$$ = ret;
}
| instr {
	list<RetInstr*>* ret = new list<RetInstr*>();
	ret->push_front((RetInstr*)$1);
	$$ = ret;
}
| {
	list<RetInstr*>* ret = new list<RetInstr*>();
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

	InstrTupleInstr* var_sym_instr = new InstrTupleInstr();
	var_sym_instr->instrs = new list<RetInstr*>();
	var_sym_instr->instrs->push_back(var_sym);

	SymbolInstr* def = new SymbolInstr();
	def->name = "define";
	
	CallInstr* ret = new CallInstr();
	ret->ref = def;
	ret->params = new ValueTupleInstr();
	ret->params->instrs = new list<RetInstr*>();
	ret->params->instrs->push_back(var_type);
	ret->params->instrs->push_back(var_sym_instr);
	
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

	InstrTupleInstr* func_sym_instr = new InstrTupleInstr();
	func_sym_instr->instrs = new list<RetInstr*>();
	func_sym_instr->instrs->push_back(func_sym);
	
	InstrTupleInstr* params = (InstrTupleInstr*)$4;
	
	SymbolInstr* def = new SymbolInstr();
	def->name = "defun";
	
	CallInstr* ret = new CallInstr();
	ret->ref = def;
	ret->params = new ValueTupleInstr();
	ret->params->instrs = new list<RetInstr*>();
	ret->params->instrs->push_back(func_type);
	ret->params->instrs->push_back(func_sym_instr);
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
	ret->instrs = (list<RetInstr*>*)$2;
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
: params_tuple_begin param_list params_tuple_end {
	InstrTupleInstr* ret = new InstrTupleInstr();
	ret->instrs = (list<RetInstr*>*)$2;
	$$ = ret;
}
;

params_tuple_begin
: '('
;

params_tuple_end
: ')'
;

param_list
: param_list_element ',' param_list {
	list<RetInstr*>* ret = (list<RetInstr*>*)$3;
	ret->push_front((RetInstr*)$1);
	$$ = ret;
}
| param_list_element {
	list<RetInstr*>* ret = new list<RetInstr*>();
	ret->push_front((RetInstr*)$1);
	$$ = ret;
}
| {
	list<RetInstr*>* ret = new list<RetInstr*>();
	$$ = ret;
}
;

param_list_element
: var_def_instr {
	$$ = $1;
}
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
	right->instrs = new list<RetInstr*>();
	right->instrs->push_back((RetInstr*)$3);

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

void ctx_print(Context* ctx, int indent = 0) {
  for(int i = 0 ; i < indent ; i++) cout << " ";
  cout << ctx->name;
  if(ctx->type) {
    cout << " -> ";
    cout << ctx->type->name;
  }
  cout << endl;
  for(auto it = ctx->children.begin() ; it != ctx->children.end() ; it++) {
    ctx_print(*it, indent+1);
  }
  if(ctx->next) {
    ctx_print(ctx->next, indent);
  }
};

Context* find(Context* cur, string name) {
	if(!cur) {
		return nullptr;
	}
	
	if(cur->name == name) {
		return cur;
	}
	else if(cur->previous) {
		return find(cur->previous, name);
	}
	else {
		return nullptr;
	}
}

void println_int(int val) { cout << val << endl; }
void println_str(string val) { cout << val << endl; }

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

  cout << global->str() << endl;

  Context* root = new Context();
  root->name = "root";

  Context* type = new Context();
  type->name = "type";
  type->type = type;

  root->children.push_back(type);

  Context* int_type = new Context();
  int_type->name = "int";
  int_type->type = type;

  int_type->previous = type;
  type->next = int_type;

  Context* s_type = new Context();
  s_type->name = "string";
  s_type->type = type;

  s_type->previous = int_type;
  int_type->next = s_type;

  Context* f_type = new Context();
  f_type->name = "fn";
  f_type->type = type;

  f_type->previous = s_type;
  s_type->next = f_type;

  Context* println_int_f = new Context();
  println_int_f->name = "println";
  println_int_f->type = f_type;
  println_int_f->value = (void*)println_int;

  println_int_f->previous = f_type;
  f_type->next = println_int_f;

  Context* println_int_arg1 = new Context();
  println_int_arg1->name = "$1";
  println_int_arg1->previous = println_int_f;
  println_int_arg1->type = int_type;

  println_int_f->children.push_back(println_int_arg1);
  
  Context* println_s_f = new Context();
  println_s_f->name = "println";
  println_s_f->type = f_type;
  println_s_f->value = (void*)println_str;

  println_s_f->previous = println_int_f;
  println_int_f->next = println_s_f;

  Context* println_s_arg1 = new Context();
  println_s_arg1->name = "$1";
  println_s_arg1->previous = println_s_f;
  println_s_arg1->type = s_type;

  println_s_f->children.push_back(println_s_arg1);

  Context* cur = println_s_f;
  
  ctx_print(root);

  for(auto it = global->instrs->begin() ; it != global->instrs->end() ; it++) {
	if((*it)->isRefInstr()) {
	    RefInstr* rinstr = (RefInstr*)(*it);
	    if(rinstr->isCallInstr()) {
	    	CallInstr* cinstr = (CallInstr*)rinstr;
			if(cinstr->ref->isSymbolInstr()) {
				if(cinstr->params->instrs->size() == 1 && cinstr->params->instrs->front()->isValInstr()) {
		  			auto vparam = (ValInstr*)(cinstr->params->instrs->front());
					if(vparam->isStringInstr()) {
			  			Context* found = find(cur, ((SymbolInstr*)cinstr->ref)->name);
						while(found) {
							if(found->children.front()->type->name == "string") {
								((void(*)(string))found->value)(((StringInstr*)vparam)->value);
								break;
							}
							found = find(found->previous, ((SymbolInstr*)cinstr->ref)->name);
						}
					}
					if(vparam->isIntegerInstr()) {
			  			Context* found = find(cur, ((SymbolInstr*)cinstr->ref)->name);
						while(found) {
							if(found->children.front()->type->name == "int") {
								((void(*)(int))found->value)(((IntegerInstr*)vparam)->value);
								break;
							}
							found = find(found->previous, ((SymbolInstr*)cinstr->ref)->name);
						}
					}
		      	}
			}
		}
	}
  }

  free (file_name);
  return 0;
}

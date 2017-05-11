#ifndef ALL_HPP
#define ALL_HPP

#include <string>
#include <iostream>
#include <vector>

using namespace std;

struct Instruction;
struct ValInstruction;
struct DefInstruction;

struct StringInstruction;
struct IntegerConstantInstruction;

struct SymbolExpr;
struct Symbol;
struct DotSymbolExpr;

struct Tuple;
struct InstrBlock;
struct Call;

struct Visitor {
  virtual void visit(Instruction* instr) = 0;
};

struct Instruction {
  virtual string str(void) = 0;

  virtual void accept(Visitor* visitor) {
    visitor->visit(this);
  }
};

struct ValInstruction : Instruction {};

struct StringInstruction : ValInstruction {
  string value;

  virtual string str(void) {
    return "\"" + value + "\"";
  }
};

struct IntegerConstantInstruction : ValInstruction {
  int value;

  virtual string str(void) {
    return to_string(value);
  }
};

struct Symbol;

struct SymbolExpr : ValInstruction {
  virtual string str(void) = 0;
  virtual Symbol* last(void) = 0;
};

struct TemplateList : vector<ValInstruction*> {
  virtual string str(void) {
    string ret = "";
    for(auto it = rbegin() ; it != rend() ; it++) {
      if(it != rbegin()) {
	ret += ",";
      }
      ret += (*it)->str();
    }
    return ret;
  }
};

struct Symbol : SymbolExpr {
  string name;
  TemplateList* tlist;

  virtual string str(void) {
    if(tlist != NULL) {
      return name + "<" + tlist->str() + ">";
    }
    return name;
  }

  virtual Symbol* last(void) {
    return this;
  }
};

struct DotSymbolExpr : SymbolExpr, pair<Symbol*, SymbolExpr*> {
  virtual string str(void) {
    return first->str() + "." + second->str();
  }

  virtual Symbol* last(void) {
    return second->last();
  }
};

struct Tuple : vector<ValInstruction*> {
  virtual string str(void) {
    string ret = "";
    for(auto it = rbegin() ; it != rend() ; it++) {
      if(it != rbegin()) {
	ret += ",";
      }
      ret += (*it)->str();
    }
    return "(" + ret + ")";
  }
};

struct InstrBlock : ValInstruction, vector<Instruction*> {
  virtual string str(void) {
    string ret = "";
    for(auto it = rbegin() ; it != rend() ; it++) {
      if(it != rbegin()) {
	ret += ";";
      }
      ret += (*it)->str();
    }
    return "{" + ret + "}";
  }
};

struct Call : ValInstruction {
  SymbolExpr* symbol;
  Tuple* tuple;

  virtual string str(void) {
    string more = "";
    if(tuple != NULL) {
      more += tuple->str();
    }
    return symbol->str() + more;
  }
};

struct VarDecl {
  string name;
  SymbolExpr* type;

  InstrBlock* symbolInstr(void) {
    auto sname = new Symbol();
    sname->name = name;
    sname->tlist = NULL;
    auto sinstr = new InstrBlock();
    sinstr->push_back(sname);
    return sinstr;
  }
};

struct FuncDecl : VarDecl {
  SymbolExpr* return_type;
  InstrBlock* params;
};

#endif//ALL_HPP

#ifndef ALL_HPP
#define ALL_HPP

#include <string>
#include <iostream>
#include <vector>

using namespace std;

struct Instruction {
  virtual string str(void) {
    return ";";
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
  virtual string str(void) {
    return "";
  }

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

struct InstrBlock : vector<Instruction*> {
  virtual string str(void) {
    string ret = "";
    for(auto it = rbegin() ; it != rend() ; it++) {
      ret += (*it)->str();
      ret += ";";
    }
    return "{" + ret + "}";
  }
};

struct Call : ValInstruction {
  SymbolExpr* symbol;
  Tuple* tuple;
  InstrBlock* block;

  virtual string str(void) {
    string more = "";
    if(tuple != NULL) {
      more += tuple->str();
    }
    if(block != NULL) {
      more += block->str();
    }
    return "call " + symbol->str() + more;
  }
};

struct VarDecl {
  string name;
  SymbolExpr* type;

  virtual string str(void) {
    return type->str() + " " + name;
  }
};

struct DefInstruction : Instruction {
  VarDecl* decl;
  ValInstruction* value;

  virtual string str(void) {
    string more = "";
    if(value != NULL) {
      more += " = " + value->str();
    }
    return "def " + decl->str() + more;
  }
};

struct Params : vector<DefInstruction*> {
  virtual string str(void) {
    string ret = "";
    for(auto it = rbegin() ; it != rend() ; it++) {
      ret += (*it)->str();
    }
    return "(" + ret + ")";
  }

  Tuple* typeTuple(void) {
    auto ret = new Tuple();
    for(auto it = begin() ; it != end() ; it++) {
      ret->push_back((*it)->decl->type);
    }
    return ret;
  }
};

#endif//ALL_HPP

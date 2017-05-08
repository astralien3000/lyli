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
    return "\"" + value + "\";";
  }
};

struct IntegerConstantInstruction : ValInstruction {
  int value;

  virtual string str(void) {
    return to_string(value) + ";";
  }
};

struct SymbolExpr {
  virtual string str(void) {
    return "";
  }
};

struct Symbol : SymbolExpr {
  string name;

  virtual string str(void) {
    return name;
  }  
};

struct TemplateList : vector<ValInstruction*> {};

struct TemplatedSymbol : Symbol {
  TemplateList* tlist;

  virtual string str(void) {
    return name + "<...>";
  }
};

struct DotSymbolExpr : SymbolExpr, pair<Symbol*, SymbolExpr*> {
  virtual string str(void) {
    return first->str() + "." + second->str();
  }
};

struct SymbolInstruction : ValInstruction {
  SymbolExpr* symbol;

  virtual string str(void) {
    return symbol->str() + ";";
  }
};

struct Tuple : vector<ValInstruction*> {
  virtual string str(void) {
    string ret = "";
    for(auto it = rbegin() ; it != rend() ; it++) {
      ret += (*it)->str();
    }
    return "(" + ret + ");";
  }
};

struct InstrBlock : vector<Instruction*> {
  virtual string str(void) {
    string ret = "";
    for(auto it = rbegin() ; it != rend() ; it++) {
      ret += (*it)->str();
    }
    return "{" + ret + "};";
  }
};

struct Call : ValInstruction {
  SymbolExpr* symbol;
  Tuple* tuple;
  InstrBlock* block;

  virtual string str(void) {
    string more = "";
    if(tuple != NULL) {
      more += "(...)";
    }
    if(block != NULL) {
      more += "{...}";
    }
    return "call " + symbol->str() + more + ";";
  }
};

#endif//ALL_HPP

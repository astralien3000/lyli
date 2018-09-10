#ifndef ALL_HPP
#define ALL_HPP

#include <string>
#include <iostream>
#include <list>

using namespace std;

struct Instr;
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
  virtual void visit(Instr* instr) = 0;
};

struct Instr {
  virtual string str(void) = 0;

  virtual void accept(Visitor* visitor) {
    visitor->visit(this);
  }
};

struct Global {
  list<Instr*>* instrs;

  virtual string str(void) {
    string ret = "";
	for(auto it = instrs->begin() ; it != instrs->end() ; it++) {
		if(it != instrs->begin()) {
			ret += ";\n";
		}
		ret += (*it)->str();
	}
	return ret;
  }
};

struct RetInstr : Instr {};

struct ValInstr : RetInstr {};

struct StringInstr : ValInstr {
  string value;

  virtual string str(void) {
    return "\"" + value + "\"";
  }
};

struct IntegerInstr : ValInstr {
  int value;

  virtual string str(void) {
    return std::to_string(value);
  }
};

struct IntegerConstantInstr : ValInstr {
  int value;

  virtual string str(void) {
    return to_string(value);
  }
};

struct InstrTupleInstr : ValInstr {
  list<Instr*>* instrs;

  virtual string str(void) {
    string ret = "";
	ret += "{";
	for(auto it = instrs->begin() ; it != instrs->end() ; it++) {
		if(it != instrs->begin()) {
			ret += ";";
		}
		ret += (*it)->str();
	}
	ret += "}";
	return ret;
  }
};

struct ValueTupleInstr : ValInstr {
  list<RetInstr*>* instrs;

  virtual string str(void) {
    string ret = "";
	ret += "(";
	for(auto it = instrs->begin() ; it != instrs->end() ; it++) {
		if(it != instrs->begin()) {
			ret += ",";
		}
		ret += (*it)->str();
	}
	ret += ")";
	return ret;
  }
};

struct RefInstr : RetInstr {};

struct SymbolInstr : RefInstr {
  string name;

  virtual string str(void) {
    return name;
  }
};

struct CallInstr : RefInstr {
  RefInstr* ref;
  ValueTupleInstr* params;

  virtual string str(void) {
    string ret = ref->str();
    ret += params->str();
	  return ret;
  }
};

struct Unsupported : RefInstr {
  virtual string str(void) {
    return "NOT_SUPPORTED";
  }
};

#endif//ALL_HPP

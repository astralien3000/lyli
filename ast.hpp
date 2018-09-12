#ifndef ALL_HPP
#define ALL_HPP

#include <string>
#include <iostream>
#include <list>

using namespace std;

struct RetInstr {
  virtual string str(void) = 0;
};

struct Global {
  list<RetInstr*>* instrs;

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
    return to_string(value);
  }
};

struct InstrTupleInstr : ValInstr {
  list<RetInstr*>* instrs;

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

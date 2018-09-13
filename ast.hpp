#ifndef ALL_HPP
#define ALL_HPP

#include <string>
#include <iostream>
#include <list>

using namespace std;

struct RetInstr {
  virtual string str(void) = 0;

  virtual bool isValInstr(void) { return false; }
  virtual bool isRefInstr(void) { return false; }
};

struct ValInstr : RetInstr {
  bool isValInstr(void) override { return true; }

  virtual bool isStringInstr(void) { return false; }
  virtual bool isIntegerInstr(void) { return false; }
  virtual bool isInstrTupleInstr(void) { return false; }
  virtual bool isValueTupleInstr(void) { return false; }
};

struct StringInstr : ValInstr {
  string value;

  bool isStringInstr(void) override { return true; }

  virtual string str(void) {
    return "\"" + value + "\"";
  }
};

struct IntegerInstr : ValInstr {
  int value;

  bool isIntegerInstr(void) override { return true; }

  virtual string str(void) {
    return to_string(value);
  }
};

struct InstrTupleInstr : ValInstr {
  list<RetInstr*>* instrs;

  bool isInstrTupleInstr(void) override { return true; }

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

struct Global : InstrTupleInstr {
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

struct ValueTupleInstr : ValInstr {
  list<RetInstr*>* instrs;

  bool isValueTupleInstr(void) override { return true; }

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

struct RefInstr : RetInstr {
  bool isRefInstr(void) override { return true; }

  virtual bool isSymbolInstr(void) { return false; }
  virtual bool isCallInstr(void) { return false; }
};

struct SymbolInstr : RefInstr {
  string name;

  bool isSymbolInstr(void) override { return true; }

  virtual string str(void) {
    return name;
  }
};

struct CallInstr : RefInstr {
  RefInstr* ref;
  ValueTupleInstr* params;

  bool isCallInstr(void) override { return true; }

  virtual string str(void) {
    string ret = ref->str();
    ret += params->str();
	  return ret;
  }
};

struct Unsupported : RetInstr {
  virtual string str(void) {
    return "NOT_SUPPORTED";
  }
};

#endif//ALL_HPP

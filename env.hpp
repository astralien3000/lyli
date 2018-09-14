#ifndef CTX_HPP
#define CTX_HPP

#include <map>

struct SymbolTypeKey {
    string symbol;
    string type;
};

bool operator<(const SymbolTypeKey& left, const SymbolTypeKey& right) {
    return left.symbol < right.symbol || (left.symbol == right.symbol  && left.type < right.type);
}

struct Env : map<SymbolTypeKey, void*> {
    Env* previous; 
};

#endif//CTX_HPP
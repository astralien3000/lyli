#ifndef CTX_HPP
#define CTX_HPP

#include <list>

struct Context {
    Context* previous;
    Context* next;

    list<Context*> children;

    string name;
    Context* type;
    void* value;
};

#endif//CTX_HPP
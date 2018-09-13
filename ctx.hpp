#ifndef CTX_HPP
#define CTX_HPP

#include <list>

struct Context {
    Context* previous;
    Context* next;

    Context* child;

    string name;
    Context* type;
    void* value;

    Context(string name, Context* type, void* value = nullptr)
        : name(name), type(type), value(value)
        , child(nullptr), previous(nullptr), next(nullptr) {
    }

    void setPrevious(Context* prev) {
        this->previous = prev;
        if(prev) {
            prev->next = this;
        }
    }

    void setParent(Context* parent) {
        this->previous = parent;
        if(parent) {
            parent->child = this;
        }
    }
};

#endif//CTX_HPP
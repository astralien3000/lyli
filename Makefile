LEX=lex
YACC=bison -y
CFLAGS=-Wall
CC=gcc
CXX=g++

GRAMMAR=grammar.y
LEXER=lexer.l

all:parse

parse: $(GRAMMAR).cpp.o $(LEXER).c.o $(SOURCES)
	$(CXX) $(CFLAGS) $^ -o $@

%.c.o: %.c
	$(CC) -c $^ -o $@

%.cpp.o: %.cpp
	$(CXX) -c $^ -o $@

%.y.hpp %.y.cpp: %.y
	$(YACC) -d $^ -o $@

%.l.c: %.l
	$(LEX) -o $@ $^

clean:
	rm -f *.cpp.o *.c.o
	rm -f *.y.cpp *.y.hpp
	rm -f *.l.c

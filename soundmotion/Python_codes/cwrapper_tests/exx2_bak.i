%module exx2

%{
#include "exx2.h"

%}

abc::abc();
abc::~abc();
int abc::trythis(int x);

%include "exx2.h"


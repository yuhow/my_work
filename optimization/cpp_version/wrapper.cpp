extern "C" {
#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"
}

#include <iostream>

using namespace std;

extern "C" {
void setulb_(int *n, int *m,double *x,double *l,double *u,int *nbd, double *f, \
             double *g,double *factr,double *pgtol,double *wa,int *iwa, \
             char *task, int *len_task, int *iprint, int *lsave,int *isave,double *dsave);
}

extern "C" int test_cpp(lua_State *L) {

   int ii = lua_tonumber(L, 1);
   float ff = lua_tonumber(L, 2);

   cout<<"ii = "<<ii<<endl;
   cout<<"ff = "<<ff<<endl;

   return 1;
}

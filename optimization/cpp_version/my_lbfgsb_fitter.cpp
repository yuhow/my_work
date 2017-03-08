
extern "C" {
#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"
}

#include <iostream>
#include <fstream>
#include <vector>
#include <math.h>
#include <ctype.h>
#include <map>
//#include <memory>
//#include <iomanip>  // for setting I/O format of cout, ex:the precision of digit
#include <string.h>
#include <stdlib.h>  // for using random number generator
#include <time.h>

using namespace std;

double func(double *, vector<double> &, vector<double> &);
void approx_prime(const int, \
                  double*, \
                  double (*f)(double *, vector<double> &, vector<double> &), \
                  double, \
                  vector<double> &, vector<double> &, \
                  double*, double*);

extern "C" {
void setulb_(const int *n,     const int *m,      double *x,     double *l, \
             double    *u,     int       *nbd,    double *f,     double *g, \
             double    *factr, double    *pgtol,  double *wa,    int    *iwa, \
             char      *task,  int       *iprint, char   *csave, \
             int       *lsave, int       *isave,  double *dsave);
}

extern "C" int local_test_lbfgsb_fitter(lua_State *L) {
    
    // user-defined function, 3 parameters
    double init_values[3] = {1.0, 1.0, 1.0};  // 64 bits
    double mybounds[3][2] = {{0, 10}, {0, 1000}, {0 ,100}};

    double m_true = 2.5;
    double n_true = 0.5;
    double b_true = 1.0;

    vector<double> x_true;
    vector<double> y_true;
    vector<double> y_true_bias;
    double f_value[1];
    //vector<double> grad = {0.0, 0.0, 0.0};

    // random number extracted uniformly from [10, 50]
    //unsigned seed;
    //seed = (unsigned)time(NULL);
    //srand(seed);
    double low = 10.0;
    double up  = 50.0;

    double x_tmp = -3;
    while(x_tmp < 7) {
        double y_tmp = m_true*x_tmp + n_true*x_tmp*x_tmp*x_tmp + b_true;
        x_true.push_back(x_tmp);
        y_true.push_back(y_tmp);
        y_true_bias.push_back(y_tmp + ((up - low)*rand()/RAND_MAX));
        x_tmp += 0.2;
    }

    // output data
    ofstream fout("my_data.txt");
    if(!fout) {
        cout<<"can't overwrite 'my_data.txt'"<<endl;
        return 1;
    }

    fout<<"x_true"<<"\t"<<"y_true"<<"\t"<<"y_true_bias"<<endl;
    for(int i = 0; i < x_true.size(); i++) {
        fout<<x_true[i]<<"\t"<<y_true[i]<<"\t"<<y_true_bias[i]<<endl;
    }
    
    fout.close();    

    //passing the following objects to fortran routines
    //maybe static type is a good choice
    char task[60] = "START";
    char csave[60];
    int  lsave[4]; // 32 bits

    const int m(20), n(sizeof(init_values)/sizeof(*init_values));

    int iprint(1);
    int nbd[n]; // 32 bits
    int iwa[3*n]; // 32 bits
    int isave[44]; // 32 bits

    double   f(0); // 64 bits
    double   factr(10); 
    double   pgtol(1e-5);
    double   l[n]; // 64 bits
    double   u[n]; // 64 bits
    double   g[n]; // 64 bits
    double   wa[2*m*n + 4*n + 12*m*m + 12*m]; // 64 bits
    double   dsave[29]; // 64 bits

    long int maxfun(15000);

    double l__, u__;
    for(int i = 0; i < n; i++) {
        l__ = mybounds[i][0];
        u__ = mybounds[i][1];
        l[i] = l__;
        l__ = 1;
        u[i] = u__;
        u__ = 1;
        nbd[i] = 0;
    }
    
    cout<<"START L-BFGS-B optimization:"<<endl;
    cout<<"nbd = "<<nbd[0]<<", "<<nbd[1]<<", "<<nbd[2]<<endl;
    cout<<"(m, n, b) = "<<"("<<init_values[0]<<", "<<init_values[1]<<", "<<init_values[2]<<")"<<endl;

    int n_function_evals = 0;
    while(true) {
        setulb_(&n, &m, init_values, l, u, nbd, &f, g, &factr, &pgtol, wa, iwa, \
                                        task, &iprint, csave, lsave, isave, dsave);
       
        if(strncmp(task, "FG", 2) == 0) {
            //cout<<"FG operation"<<endl;
            //cout<<fixed<<setprecision(8)<<g[0]<<", "<<g[1]<<", "<<g[2]<<endl;
            //approx_prime(n, init_values, func, 1e-12, x_true, y_true, f_value, g);
            approx_prime(n, init_values, func, 1e-12, x_true, y_true_bias, f_value, g);
            //cout<<g[0]<<", "<<g[1]<<", "<<g[2]<<endl;
            f = f_value[0];
            n_function_evals += 1;
        }
        else if(strncmp(task, "NEW_X", 5) == 0) {
            //cout<<"NEW_X operation"<<endl;
            if(n_function_evals > maxfun) {
                strcpy(task, "STOP: TOTAL NO. of f AND g EVALUATIONS EXCEEDS LIMIT");
            }
        }
        else 
            break;
    }

    cout<<"END L-BFGS-B optimization:"<<endl;
    cout<<"(m, n, b) = "<<"("<<init_values[0]<<", "<<init_values[1]<<", "<<init_values[2]<<")"<<endl;
    cout<<"# of function evaluation = "<<n_function_evals<<endl;
    //task[-1] = "\n";
    cout<<task<<endl;

    return 1;
}

double func(double* params, vector<double> &args_x, vector<double> &args_y) {

    double sum_error(0.0);
    for(int i = 0; i < args_x.size(); i++) {
        double x_tmp = args_x[i];
        double y_tmp = params[0]*x_tmp + params[1]*x_tmp*x_tmp*x_tmp + params[2];
        double error = args_y[i] - y_tmp;
        sum_error += pow(error, 2);
    }
    return sum_error;
}

void approx_prime(const int ndim, \
                  double* xk, \
                  double (*f)(double*, vector<double> &, vector<double> &),\
                  double epsilon, \
                  vector<double> &args_x, vector<double> &args_y, \
                  double* f0, double* grad) {

    f0[0] = f(xk, args_x, args_y);
    double xk_tmp[ndim];
    std::copy(&xk[0], &xk[ndim], xk_tmp);
    for(int i = 0; i < ndim; i++) {
        xk_tmp[i] = xk_tmp[i] + epsilon;
        grad[i] = (f(xk_tmp, args_x, args_y) - f0[0]) / epsilon;
        xk_tmp[i] = xk_tmp[i] - epsilon;
    }
}

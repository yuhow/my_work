extern "C" {
#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"
}

#include <iostream>
#include <vector>
#include <math.h>
#include <ctype.h>
#include <map>
//#include <memory>
//#include <iomanip>  // for setting I/O format of cout, ex:the precision of digit
#include <string.h>

using namespace std;

double func(double *, vector<double> &, vector<double> &);
void approx_prime(const long int, \
                  double*, \
                  double (*f)(double *, vector<double> &, vector<double> &), \
                  double, \
                  vector<double> &, vector<double> &, \
                  double*, double*);

extern "C" {
void setulb_(const long int *n, const long int *m, double *x,    double   *l,      double *u, \
             long int *nbd,     double   *f,       double *g,    double   *factr,  double *pgtol, \
             double   *wa,      long int *iwa,     char   *task, long int *iprint, char   *csave, \
             long int *lsave,   long int *isave,   double *dsave);
}
//             long int *isave,   double   *dsave,   long int *osave);
//}

extern "C" int test1_cpp(lua_State *L) {
    
    // user-defined function, 3 parameters
    double init_values[3] = {1.0, 1.0, 1.0};
    double mybounds[3][2] = {{0, 10}, {0, 10000}, {0 ,100}};

    double m_true = 2.5;
    double n_true = 0.5;
    double b_true = 1.0;

    vector<double> x_true;
    vector<double> y_true;
    double f_value[1];
    //vector<double> grad = {0.0, 0.0, 0.0};

    //for(int i = 0; i <= 50; i++) {
    //    double x_tmp = -3 + i*0.2;
    //    double y_tmp = m_true*x_tmp + n_true*x_tmp*x_tmp*x_tmp + b_true;
    //    x_true.push_back(x_tmp);
    //    y_true.push_back(y_tmp);
    //}
    double x_tmp = -3;
    while(x_tmp < 7) {
        double y_tmp = m_true*x_tmp + n_true*x_tmp*x_tmp*x_tmp + b_true;
        x_true.push_back(x_tmp);
        y_true.push_back(y_tmp);
        x_tmp += 0.2;
    }
    
    //cout<<init_values[0]<<", "<<x_true[0]<<", "<<y_true[0]<<endl;
    //cout<<func(init_values, x_true, y_true)<<endl;
    //cout<<init_values[0]<<", "<<x_true[0]<<", "<<y_true[0]<<endl;
    
    static const long int m(20), n(sizeof(init_values)/sizeof(*init_values));
    /* System generated locals */
    long int i__1;
    double   d__1, d__2;
    /* Local variables */
    static double   f(f_value[0]);
    static double   g[n];

    static long int i__;
    static double   l[n];
    static double   u[n], x[n], t1, t2; 
    static double   wa[2*m*n + 4*n + 12*m*m + 12*m];
    static long int nbd[n], iwa[3*n];
    static char     task[60] = "START";
    
    //static long int taskValue;
    //static long int *task=&taskValue; /* must initialize !! */
/*      http://stackoverflow.com/a/11278093/269192 */
    static double   factr(10);
    static char     csave[60];
    //static long int csaveValue;
    //static long int *csave=&csaveValue;
    static double   dsave[29], dsave2[29];
    //uninitialized_fill_n(dsave, 29, 10); 
    static long int isave[44];
    static long int lsave[4];
    //static long int osave[300];
    static double   pgtol(1e-5);
    static long int iprint(-1);
    static long int maxfun(15000);

    double l__, u__;
    for(int i = 0; i < n; i++) {
        l__ = mybounds[i][0];
        u__ = mybounds[i][1];
        l[i] = l__;
        l__ = 1;
        u[i] = u__;
        u__ = 1;
        nbd[i] = 3;
    }
    
    cout<<"START L-BFGS-B optimization:"<<endl;
    cout<<"(m, n, b) = "<<"("<<init_values[0]<<", "<<init_values[1]<<", "<<init_values[2]<<")"<<endl;

    int n_function_evals = 0;
    while(true) {
        setulb_(&n, &m, init_values, l, u, nbd, &f, g, &factr, &pgtol, wa, iwa, \
                                        task, &iprint, csave, lsave, isave, dsave);

        if(strncmp(task, "FG", 2) == 0) {
            //cout<<sizeof(init_values)<<", "<<sizeof(*init_values)<<endl;
            //cout<<fixed<<setprecision(8)<<grad[0]<<", "<<grad[1]<<", "<<grad[2]<<endl;
            approx_prime(n, init_values, func, 1e-12, x_true, y_true, f_value, g);
            f = f_value[0];
            n_function_evals += 1;
            //cout<<grad[0]<<", "<<grad[1]<<", "<<grad[2]<<endl;
        }
        else if(strncmp(task, "NEW_X", 5) == 0) {
            if(n_function_evals > maxfun) {
                strcpy(task, "STOP: TOTAL NO. of f AND g EVALUATIONS EXCEEDS LIMIT");
            }
        }
        else 
            break;
    }

    cout<<"END L-BFGS-B optimization:"<<endl;
    cout<<"(m, n, b) = "<<"("<<init_values[0]<<", "<<init_values[1]<<", "<<init_values[2]<<")"<<endl;

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

void approx_prime(const long int ndim, \
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

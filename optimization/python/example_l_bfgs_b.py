"""
Praticing how to use fmin_l_bfgs_b (scipy, v0.10.0)
Which maybe can be implemented in RTP.

2017/01/17, You-Hao Chang

adjustable parameters: factr, pgtol, epsilon, maxfun
"""
import random
import numpy as np
#from lbfgsb_rtp import fmin_l_bfgs_b
from lbfgsb_rtp_animation import fmin_l_bfgs_b
import matplotlib.pyplot as plt

# data set
# random.seed(100)
x_true = np.arange(-3,7,0.2)
m_true = 2.5
n_true = 0.5
b_true = 1.0
y_true = m_true*x_true + n_true*x_true*x_true*x_true + b_true
y_true = [y_ori+random.uniform(10, 70) for y_ori in y_true]
#y_true = [y_ori+np.random.poisson(10)*5 for y_ori in y_true]

# define a function which will return the "cost"
def func(params, *args):
    x = args[0]
    y = args[1]
    m, n, b = params
    #print "m=" + str(m) + ", n=" + str(n) + ", b=" + str(b)
    y_model = m*x + n*x*x*x + b
    error = y - y_model
    return sum(error**2) 

def func2(params, *args):
    x = args[0]
    y = args[1]
    m, n, b = params
    #print "m=" + str(m) + ", n=" + str(n) + ", b=" + str(b)
    y_model = m*x + n*x*np.exp(x) + b
    error = y - y_model
    return sum(error**2) 

def approx_fprime(xk, f, epsilon, *args):
    f0 = f(*((xk,)+args))
    grad = np.zeros((len(xk),), float)
    ei = np.zeros((len(xk),), float)
    for k in range(len(xk)):
        ei[k] = epsilon
        grad[k] = (f(*((xk+ei,)+args)) - f0) / epsilon
        ei[k] = 0.0
    #print "grad = " + str(grad)
    return f0, grad

def approx_fprime_v2(xk, f, epsilon, *args):
    _epsilon = epsilon * np.random.permutation([1, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6])[0]
    print _epsilon
    f0 = f(*((xk,)+args))
    grad = np.zeros((len(xk),), float)
    ei = np.zeros((len(xk),), float)
    for k in range(len(xk)):
        ei[k] = _epsilon
        grad[k] = (f(*((xk+ei,)+args)) - f0) / _epsilon
        ei[k] = 0.0
    #print "grad = " + str(grad)
    return f0, grad

# initialize the searching point
initial_values = np.array([1.0, 0.0, 1.0])
mybounds = [(0, 10), (0, 10000), (0, 100)]
#mybounds = [(0, 10), (None, None), (0, 100)]
initial_values2 = np.array([1.0, 0.0])
mybounds2 = [(0, 10), (0, 100)]

# BFGS optimization
print initial_values
final_model = fmin_l_bfgs_b(func2, x0=initial_values, fprime=approx_fprime_v2, args=(x_true, y_true), 
                            bounds=mybounds, factr=10, pgtol=1e-5, epsilon=1e-12,
                            maxfun=15000, disp=-1)
#final_model = fmin_l_bfgs_b(func, x0=initial_values, fprime=approx_fprime, args=(x_true, y_true), 
#                            factr=10, pgtol=1e-5, epsilon=1e-8,
#                            maxfun=150000, disp=-1)

print final_model
#plt.scatter(x_true, y_true, label = 'real data')
#plt.plot(x_true, initial_values[0]*x_true + initial_values[1]*x_true*x_true*x_true + initial_values[2], color = 'r', label = 'input model')
#plt.plot(x_true, final_model[0][0]*x_true + final_model[0][1]*x_true*x_true*x_true + final_model[0][2], color = 'g', label = 'final model')
#plt.plot(x_true, final_model[0][0]*x_true + final_model[0][1])
#plt.legend()
#plt.show()

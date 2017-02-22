# 2017/2/16
# You-Hao Chang
# for C++11

FC = gfortran
CC = g++ -std=c++0x

FLAGS = -shared -fPIC -O2
LIBS = -llapack

all: froutines cwrapper my_lbfgsb_fitter
	$(CC) $(FLAGS) -o _lbfgsb.so routines.so wrapper.so
	$(CC) $(FLAGS) -o _my_lbfgsb_fitter.so routines.so my_lbfgsb_fitter.so

froutines: routines.f
	$(FC) $(FLAGS) routines.f -o routines.so $(LIBS)

cwrapper: wrapper.cpp
	$(CC) $(FLAGS) wrapper.cpp -o wrapper.so

my_lbfgsb_fitter: my_lbfgsb_fitter.cpp
	$(CC) $(FLAGS) my_lbfgsb_fitter.cpp -o my_lbfgsb_fitter.so

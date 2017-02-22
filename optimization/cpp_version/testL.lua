-- my first LUA 
-- 2017/2/17, You-Hao Chang 

--LIBPATH = "_lbfgsb.so"
--FUNCNAME = "test_cpp"
LIBPATH = "_my_lbfgsb_fitter.so"
FUNCNAME = "lbfgsb_fitter"
testFunc = package.loadlib(LIBPATH, FUNCNAME)

testFunc(1,2.2)

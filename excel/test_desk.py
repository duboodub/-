

# from data_process_oop import Excel_Book, Excel_Sheet, File
import originpro as op
import os
import numpy as np
from scipy.optimize import root_scalar, fsolve, root

def f_miu_p(p, A=1, p0=0.16,):
    print(type(p))
    if isinstance(p,(float, int, np.int32, np.float32)):
        if p<=p0:
            miu = 0
        elif p>p0:
            miu = -A*(p-p0)
        return miu
    
    elif isinstance(p,(list, np.ndarray)):
        
        miu_list = []
        for pi in p:
            miu = f_miu_p(pi,A,p0)
            miu_list.append(miu)
        return miu_list
    else:
        raise TypeError('type of p does not fit.')

# p = 4.0
# miu = f_miu_p(p,p0=3)

# p=np.array([4,4,4,4])
# # miul= miu_p(p)

# miul = f_miu_p(p,p0=3)


# miu_list = []
# m=0

# for pi in p:
#     m += pi
#     miu = f_miu_p(pi)
#     miu_list.append(miu)

from scipy.optimize import fsolve

def f(a):
    global b
    c = a+b
    return c

def fun(x):
    return [x[0]  + 0.5 * (x[0] - x[1])**3 - 1.0,
            0.5 * (x[1] - x[0])**3 + x[1]]

def jac(x):
    return np.array([[1 + 1.5 * (x[0] - x[1])**2,
                      -1.5 * (x[0] - x[1])**2],
                     [-1.5 * (x[1] - x[0])**2,
                      1 + 1.5 * (x[1] - x[0])**2]])


if __name__ == '__main__':
    
    # global b
    # b=3
    # c = [1,23,3]
    # d = f(2)
    
    # # f = c
    # f = globals()['__name__']
    
    sol = root(fun, [0, 1], method='hybr',)
    print(sol.x)
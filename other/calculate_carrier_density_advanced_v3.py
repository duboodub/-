# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 21:26:49 2021

@author: db
"""

import numpy as np
import matplotlib.pyplot as plt 
import math
from scipy.integrate import solve_bvp

def f_miu_p(p,  K1=1e-6, K2=2, p0=0.16,):
    if isinstance(p,(float, int, np.int32, np.float64)):
        miu = -K2*(p-p0)
        return miu
    
        
def f_miu_p_1(p,  K1=1e-6, K2=1.5, p0=0.16,):
    # print('type(p): %s'%(type(p)))
    if isinstance(p,(float, int, np.int32, np.float64)):
        # if p<=p0:
        #     miu = -K1*(p-p0)
        # elif p>p0:
        #     miu = -K2*(p-p0)
        miu = -K2*(p-p0)
        return miu
    
    elif isinstance(p,(list, np.ndarray)):
        
        miu_list = []
        for pi in p:
            miu = f_miu_p_1(pi,K1,K2,p0)
            miu_list.append(miu)
        return np.array(miu_list)
    
    else:
        raise TypeError('type of p does not fit.')
        
        
def f_p_miu_1(miu,  K1=1e-6, K2=1.5, p0=0.16,):
    # inverse function of miu(p)
    # print('type(p): %s'%(type(p)))
    if isinstance(miu,(float, int, np.int32, np.float64)):
        # if p<=p0:
        #     miu = -K1*(p-p0)
        # elif p>p0:
        #     miu = -K2*(p-p0)
        p = -(1/K2)*miu+p0
        return p
    
    elif isinstance(miu,(list, np.ndarray)):
        
        p_list = []
        for miu_i in miu:
            p = f_p_miu_1(miu_i,K1,K2,p0)
            p_list.append(p)
        return np.array(p_list)
    
    else:
        raise TypeError('type of p does not fit.')
        
        
def f_xz(z,x0,lamda):
    '''
    calculate x(z)

    Parameters
    ----------
    z : TYPE
        DESCRIPTION.
    x0 : TYPE
        DESCRIPTION.
    lamda : TYPE
        DESCRIPTION.

    Raises
    ------
    TypeError
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    print('type(z): %s'%(type(z)))
    if isinstance(z,(float, np.float64)):
        if z>=0:
            x = (x0/2)*math.exp(-(z/lamda))
        elif z<0:
            x = x0 - (x0/2)*math.exp((z/lamda))
        return x
    
    elif isinstance(z,(list, np.ndarray)):
        x_list=[]
        for i,zi in enumerate(z):
            x = f_xz(zi,x0,lamda)
            x_list.append(x)
        return x_list
            
    else:
        raise TypeError('type of z does not fit.')
     
def f_p_miu_eq(miu_i1,miu_i2,miu_i3,xi,dzi, A):
    pi = xi-(miu_i1 + miu_i3 - 2*miu_i2)/(A)
    return pi
    
def p_i_list_iter(p_i_list,x_i_list,dzi,A):
    miu_i_list = f_miu_p_1(p_i_list)
    for i in range(1, len(p_i_list)-1):
        p_i_list[i]=f_p_miu_eq(miu_i_list[i-1],miu_i_list[i],miu_i_list[i+1],x_i_list[i],dzi,A)
    return p_i_list
    
    
def f_get_M(dim):
    M = np.zeros((dim, dim))
    M[0, 0] = 1
    M[dim-1, dim-1] = 1
    for i in range(1, dim-1):
        M[i, i-1] = 1
        M[i, i] = -2
        M[i, i+1] = 1
    print(M)
    return M
        

def f_get_b(p_i_list, x_i_list,A):
    b = -A*(p_i_list-x_i_list)
    b[0] = f_miu_p_1(p_i_list[0])
    b[l-1] = f_miu_p_1(p_i_list[l-1])
    return b


def F():
    pass

if __name__ == '__main__':
    #input
    n=10
    m=1
    c = 1.32E-4
    c = 1
    
    lamda = 0.5*c
    x0 = 0.4
    
    A = 1
    # x_i_list = np.array(f_xz(z_i_list,x0,lamda))
    
    dzn = c/2
    dzi = dzn/m
    
    
    i_list = np.arange((2*n-1)*m+1)
    z_i_list = dzi*i_list - (n*dzn - dzn/2)

    x_i_list = np.array(f_xz(z_i_list,x0,lamda))
    l_hf = int(len(z_i_list)/2)
    # x_i_list = np.array( list(np.ones(l_hf))+list(np.zeros(l_hf)) )
    # x_i_list = np.arange(len(z_i_list))/len(z_i_list)
    
    # x_i_list
    # lx = len(z_i_list)
    # x_i_list=[]
    # for i in range(lx):
    #     x_i_list.append(pow((i-lx/2),2))
        
    # x_i_list= np.array(x_i_list)
    
    p_i_list = 1*np.ones(len(x_i_list))
    p_i_list = x_i_list.copy()
    # p_i_list = np.arange(len(z_i_list))/len(z_i_list)
    miu_i_list = f_miu_p_1(p_i_list)
    
    l = len(x_i_list)
    
    M = f_get_M(l)
    b = f_get_b(p_i_list, x_i_list,A)

    # i1 = int(l/2)-3
    # i2 = int(l/2)+3
    i1 = 0
    i2 = l
    
    fig, ax1 = plt.subplots()
    ax1.plot(i_list, x_i_list, label='x_i_list',)
    ax1.set_title('x_i_list')
    plt.show()
    
    for i in range(10):


        fig, ax1 = plt.subplots()
        ax1.plot(i_list[i1:i2], p_i_list[i1:i2])
        # ax1.plot(i_list[i1:i2], x_i_list[i1:i2], label='x_i_list',)
        # ax1.semilogy(i_list[i1:i2], p_i_list[i1:i2])
        # ax1.plot(i_list[i1:i2], p_i_list[i1:i2]-x_i_list[i1:i2], label='x_i_list',)
        
        ax1.set_title('p_i_list, step:%d'%i)
        plt.show()
        
        # fig, ax1 = plt.subplots()
        # ax1.plot(i_list[i1:i2], p_i_list[i1:i2]-x_i_list[i1:i2], label='x_i_list',)
        # ax1.set_title('p-x_i_list, step:%d'%i)
        # plt.show()
        
        b = f_get_b(p_i_list, x_i_list,A)
        miu_i_list = np.linalg.solve(M, b)
        p_i_list = f_p_miu_1(miu_i_list,)
        
    Q=f_p_miu_eq(1,2,4,0,1,1)




























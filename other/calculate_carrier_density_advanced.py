# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 14:26:20 2021

@author: db
"""

import numpy as np
import matplotlib.pyplot as plt 
import math

def zi_list_from_ilist(i_list, dz:int):
    zi_list = []        # z of nth layer
    for i in i_list:
        if i<= 0:
            zi = dz*i + dz/2
        else:
            zi = dz*i - dz/2
        zi_list.append(zi)
        
    return np.array(zi_list)

def f_i_n_list(i_list, m):
    i_n_list = []
    l=len(i_list)
    j = 0
    while j<l:
        i_n_list.append( i_list[j] )
        j += m
    return np.array(i_n_list)
    
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
        
def f_miu_p(p, A=1, p0=0.16,):
    # print('type(p): %s'%(type(p)))
    if isinstance(p,(float, int, np.int32, np.float64)):
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
        return np.array(miu_list)
    
    else:
        raise TypeError('type of p does not fit.')

def f_miu_p_1(p, A=1, A1=1e-2, p0=0.16,):
    '''
    calculate miu from p with slope not zero.

    Parameters
    ----------
    p : TYPE
        DESCRIPTION.
    A : TYPE, optional
        DESCRIPTION. The default is 1.
    p0 : TYPE, optional
        DESCRIPTION. The default is 0.16.

    Raises
    ------
    TypeError
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    # print('type(p): %s'%(type(p)))
    if isinstance(p,(float, int, np.int32, np.float64)):
        if p<=p0:
            miu = -A1*(p-p0)
        elif p>p0:
            miu = -A*(p-p0)
        return miu
    
    elif isinstance(p,(list, np.ndarray)):
        
        miu_list = []
        for pi in p:
            miu = f_miu_p_1(pi,A,A1,p0)
            miu_list.append(miu)
        return np.array(miu_list)
    
    else:
        raise TypeError('type of p does not fit.')
        
def f_p_miu_1(miu, A=1, A1=1, p0=0.16, ):
    '''
    calculate p from miu.

    Parameters
    ----------
    miu : TYPE
        DESCRIPTION.
    A : TYPE, optional
        DESCRIPTION. The default is 1.
    B : TYPE, optional
        DESCRIPTION. The default is 1e-2.
    p0 : TYPE, optional
        DESCRIPTION. The default is 0.16.
     : TYPE
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
    # print('type(p): %s'%(type(p)))
    if isinstance(miu,(float, int, np.int32, np.float64)):
        if miu>=0:
            p = -(1/A1)*miu + p0
        elif miu <0:
            p = -(1/A)*miu +p0
        return p
    
    elif isinstance(miu,(list, np.ndarray)):
        
        p_list = []
        for miui in miu:
            p = f_p_miu_1(miu,A,A1,p0)
            p_list.append(p)
        return np.array(p_list)
    
    else:
        raise TypeError('type of miu does not fit.')
        


def f_B(epsilon_0, epsilon_r, a, c, e=1.602176634e-19):
    return  2*e*e/(epsilon_0*epsilon_r*a*a*c)


def iteration_1(p_i_list, x_i_list, dzi, B, steps=2):
    miu_i_list = f_miu_p_1(p_i_list)
    pt = plt.plot(np.arange(len(p_i_list)), p_i_list, label='p_i_list',)
    plt.title('p_i_list, step:-1')
    plt.show()
    
    # p_i_list_1 = p_i_list.copy()
    for s in range(steps):
        miu_i_list = f_miu_p_1(p_i_list)
        for i in range( 1, len(p_i_list)-1 ):
            c = -B*( p_i_list[i]- x_i_list[i]) + 2*miu_i_list[i] - miu_i_list[i-1]
            miu_i_list[i+1] = c
            p_i_list[i+1] = f_p_miu_1(miu_i_list[i+1],)
            
            
        fig, (ax1,ax2) = plt.subplots(ncols=2)
        fig.set_size_inches(14.0,7.0)
        ax1.semilogy(np.arange(len(p_i_list)), p_i_list)
        ax1.set_title('p_i_list, step:%d'%s)
        
        ax2.plot(np.arange(len(p_i_list)), p_i_list)
        plt.show()
        
        # p_i_list = p_i_list_1.copy()
        
    return p_i_list

def iteration(p_i_list, x_i_list, dzi, B, steps=2):
    miu_i_list = f_miu_p(p_i_list)
    pt = plt.plot(np.arange(len(p_i_list)), p_i_list, label='p_i_list',)
    plt.title('p_i_list, step:-1')
    plt.show()
    
    p_i_list_1 = p_i_list.copy()
    for s in range(steps):
        miu_i_list = f_miu_p(p_i_list)
        for i in range( len(p_i_list) ):
            if (i == 0) or (i == (len(p_i_list)-1)):
                p_i_list_1[i] = p_i_list[i]
            else:
                p_i_list_1[i] = x_i_list[i] - (miu_i_list[i+1] + miu_i_list[i-1] - 2*miu_i_list[i]) / (dzi*dzi*B)
        
        fig, (ax1,ax2) = plt.subplots(ncols=2)
        fig.set_size_inches(12.0,8.0)
        ax1.semilogy(np.arange(len(p_i_list)), p_i_list)
        ax2.plot(np.arange(len(p_i_list)), p_i_list)
        ax1.set_title('p_i_list, step:%d'%s)
        plt.show()
        
        p_i_list = p_i_list_1.copy()
        
    return p_i_list

if __name__ == '__main__':
    
    ## input a: , x[]:dopants density,  
    ## -> p[]: hole carrier density
    
    # n boundary
    n = 100
    c = 1.32E-9
    
    dzn = c/2
    
    n_list = np.array(list(range(-n, 0)) + list(range(1, n+1)))
    zn_list = zi_list_from_ilist(n_list, dzn)
    # zn_list = 
    
    
    
    # input devide c/2 into m
    m = 1
    dzi = dzn/m
    
    i_list = np.arange((2*n-1)*m+1)
    i_n_list = f_i_n_list(i_list, m)
    
    
    z_i_list = dzi*i_list - (n*dzn - dzn/2)
    
    # input
    x0 = 0.2
    lamda = c/2
    x_i_list = np.array(f_xz(z_i_list,x0,lamda))
    fg = plt.figure()
    pt = plt.plot(np.arange(len(x_i_list)), x_i_list, label='x_i_list',)
    plt.title('x_i_list')
    plt.show()
        
    # input
    # p_i_list = np.linspace(x0, 0, len(i_list))
    p_i_list = x_i_list
    miu_i_list = f_miu_p_1(p_i_list)
    
    B = 1
    p_i_list = iteration_1(p_i_list, x_i_list, dzi, B, steps= 15 )
    
    
    # distance
    
    # a=1
    # x=np.array([1,1,0,0,1,1])
    # xi= 0.45
    
    
    # x = x*xi
    # y = -a*x
    # dim = len(x)
    # A = np.eye(dim,k=1) + np.eye(dim,k=-1) - np.eye(dim)*(2+a)
    # A[0,dim-1] = 1
    # A[dim-1,0] = 1
    # B = np.insert(A,dim,y,axis=1)
    # p = np.linalg.solve(A,y)
    # print(p)
    
    # p_min = 0.07
    # p_max = 0.2
    # T_s = 9000
    # # p[2]=0.165
    # T_ph = (p_max - p[2])*(p[2]-p_min)*T_s
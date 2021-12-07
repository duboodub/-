# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 19:21:39 2021

@author: db
"""

import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.integrate import solve_bvp,solve_ivp

def f_miu_p_1(p,  K1=1e-6, K2=1.5, p0=0.16,):
    # print('type(p): %s'%(type(p)))
    if isinstance(p,(float, int, np.int32, np.float64)):
        if p<=p0:
            miu = -K1*(p-p0)
        elif p>p0:
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
        
        
def f_layer_index_list(l_a, l_b=None,):
    '''
    return a layer_index_list given the boundary layer index.

    Parameters
    ----------
    l_a : TYPE
        DESCRIPTION.
    l_b : TYPE, optional
        DESCRIPTION. The default is None.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    if l_b == None:
        l_b = l_a
        l_a = -l_b
    
    if isinstance(l_a,(float)):
        l_a = int(l_a)
    if isinstance(l_b,(float)):
        l_b = int(l_b)
        
    if isinstance(l_a,(int)) and isinstance(l_b,(int)):
        layer_index_list = []
        if l_a <= l_b:
            l = l_a
            while l <= l_b:
                if l != 0:
                    layer_index_list.append(l)
                l += 1
                
        elif l_a > l_b:
            l = l_a
            while l >= l_b:
                if l != 0:
                    layer_index_list.append(l)
                l -= 1
        return layer_index_list
    
    else:
        raise TypeError('layer_index must be int type.')


def f_z_layer(layer_index, dz):
    if isinstance(layer_index,(int)):
        if layer_index > 0:
            z_l = dz * layer_index - dz/2
        elif layer_index < 0:
            z_l = dz *layer_index + dz/2
        elif layer_index == 0:
            raise ValueError('layer_index shouldn\'t be 0.')
        return z_l
    
    elif isinstance(layer_index, (list, np.ndarray)):
        z_l_list = []
        for l in layer_index:
            z_l = f_z_layer(l, dz)
            z_l_list.append(z_l)
        return z_l_list
    
    else:
        raise TypeError('type of layer_index in f_z_layer() does not fit.')
        
        
def f_xz(z,x0=0.4,lamda=1e-9):
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
    # print('type(z): %s'%(type(z)))
    global dz
    lamda = dz/2
    if isinstance(z,(int, float, np.float64)):
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
        
        
def f_M_ivp(z, p, ):
    # K=[1,1], p0=1, A=1, f_xz_para={'x0':0.4,'lamda':1e-1}
    K=[1,1]
    p0=1
    A=1
    f_xz_para={'x0':0.4,'lamda':1e-5}
    if p[0]<=p0:
        p1p = -A/K[0]*(p[0]-f_xz(z, f_xz_para['x0'], f_xz_para['lamda']))
        return [p[1], p1p]
    elif p[0]>p0:
        p1p = -A/K[1]*(p[0]-f_xz(z, f_xz_para['x0'], f_xz_para['lamda']))
        return [p[1], p1p]    


def f_M_bvp(t,y):
    K=[1e-17,1]
    p0=0.16
    A=1
    
    ys = np.zeros(y.shape)
    ys[0] = y[1]
    
    for i,y0 in enumerate(y[0]):
        if y[0,i]<=p0:
            y1p = -A/K[0]* (y[0,i]-f_xz(t[i]))
            # print(y[0])
            # print('y1p=\n')
            # print(y1p)
            ys[1][i] = y1p
        elif y[0,i]>p0:
            y1p = -A/K[1]* (y[0,i]-f_xz(t[i]))
            ys[1][i] = y1p
    
    return ys
    

def bc_M_bvp(ya, yb):
    # a = f_xz(-50,0.4,3)
    # b = f_xz(50,0,3)
    # return [ya[0]-a, yb[0]-b]
    
    #bvp v2
    global x_bvp, dz
    a = f_xz(x_bvp[0])
    b = f_xz(x_bvp[-1])
    return [ya[0]-a, yb[0]-b]

          
def f_test(t,y,k=[1,2]):
    if y<=10:
        return k[0]
    elif y>10:
        return k[1]
    

def f_t(m,s,k1=[0,1],k2=2):
    return [s[1],k1[0]+k2]




if __name__ == '__main__':
        
    '''
    # sol= solve_ivp(f_test,[0,20],[0],args=[[1,2]],dense_output=True,t_eval=np.linspace(0,20,100))
    # sy = sol.y[0]
    # st = sol.t
    
    # fig, ax1 = plt.subplots()
    # ax1.plot(st, sy)
    # ax1.set_title('y-t')
    # plt.show()
    
    
    # sol= solve_ivp(f_t,[0,20],[0,0],args=[[1,2]],dense_output=True,t_eval=np.linspace(0,20,100))
    # sy = sol.y[0]
    # st = sol.t
    
    # fig, ax1 = plt.subplots()
    # ax1.plot(st, sy)
    # ax1.set_title('y-t')
    # plt.show()
    
    
    
    # slt = solve_ivp(f_M_ivp,[50,-5], [0,0], t_eval=np.linspace(50,-5,100),dense_output=True)
    # sy = slt.y[0]
    # st = slt.t
    # fig, ax1 = plt.subplots()
    # ax1.plot(st, sy, label='ya')
    # ax1.set_title('y-t')
    # plt.show()
    '''
    
    
    # x=np.linspace(-50,50,100000)
    
    # X = []
    # for z in x:
    #     Xi = f_xz(z,)
    #     X.append(Xi)
    
    # y=np.zeros((2,len(x)))
    # y[0]=X.copy()
    # slt = solve_bvp(f_M_bvp, bc_M_bvp, x, y,tol=1e-6)
    
    # sy = slt.y[0]
    # st = slt.x
    
    # sty = slt.sol(x)[0]
    
    # X1 = []
    # for z in st:
    #     Xi = f_xz(z,)
    #     X1.append(Xi)
    
    # # i1=int(len(st)/2)-40
    # # i2=int(len(st)/2)+10
    # i1=0
    # i2=10000
    
    # fig, ax1 = plt.subplots()
    # # ax1.plot(x[i1:i2], sty[i1:i2], label='ya')
    # ax1.plot(st, sy, label='ya')
    # ax1.plot(x[i1:i2], X[i1:i2], label='x')
    # ax1.set_title('y-t')
    # plt.show()
    
    
    # fig, ax1 = plt.subplots()
    # ax1.plot(x[i1:i2], X[i1:i2], label='x')
    # ax1.set_title('y-t')
    # plt.show()
    
    
    
    c = 1.2e-9
    dz = c/2
    layer_index_list = f_layer_index_list(1e8,)
    z_i_list = f_z_layer(layer_index_list, dz)
    x_i_list = f_xz(z_i_list)
    
    x_bvp = np.linspace(z_i_list[0], z_i_list[-1],10000)
    
    X_i_list_bvp = []
    for z in x_bvp:
        xi = f_xz(z,)
        X_i_list_bvp.append(xi)
    
    y_bvp=np.zeros((2,len(x_bvp)))
    y_bvp[0]=X_i_list_bvp.copy()
    
    sol = solve_bvp(f_M_bvp, bc_M_bvp, x_bvp, y_bvp,tol=1e-10,)
    
    p_i_list = sol.sol(z_i_list)[0]
    
    
    fig, ax1 = plt.subplots()
    # ax1.plot(x[i1:i2], sty[i1:i2], label='ya')
    # ax1.plot(layer_index_list[4995:5005], p_i_list[4995:5005], label='ya')
    ax1.plot(layer_index_list[4995:5005], x_i_list[4995:5005], label='x')
    # ax1.plot(sol.x, sol.y[0], label='x')
    
    ax1.set_title('y-t')
    plt.show()
    
    
    # fig, ax1 = plt.subplots()
    # # ax1.plot(x[i1:i2], sty[i1:i2], label='ya')
    # # ax1.plot(layer_index_list, p_i_list, label='ya')
    # # ax1.plot(layer_index_list, x_i_list, label='x')
    # ax1.plot(sol.x, sol.y[0], label='x')
    
    # ax1.set_title('y-t')
    # plt.show()  
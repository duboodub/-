# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 15:17:25 2021
欧拉法 打靶

B:      def cal_miu3_ODE(miu1,miu2,x2, B=1)
K2, p0: def f_miu_p_1(p,  K1=1e-6, K2=1.5, p0=0.16, inverse=False)
xz:     def f_xz(z,x0=0.4,lamda=1e-9)

@author: db
"""

import numpy as np
import matplotlib.pyplot as plt 
import math
from scipy.integrate import solve_bvp,solve_ivp
from scipy.optimize import root_scalar, fsolve
def f_miu_p_1(p,  K1=1.5, K2=1.5, p0=0.1, inverse=False):
    # print('type(p): %s'%(type(p)))
    if inverse == False:
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
    
    elif inverse == True:
        miu = p.copy()
        if isinstance(miu,(float, int, np.int32, np.float64)):
            if miu<=0:
                p = p0 - miu/K2
            elif miu>0:
                p = p0-miu/K1
            return p
        
        elif isinstance(miu,(list, np.ndarray)):
            
            p_list = []
            for miui in miu:
                p = f_miu_p_1(miui,K1,K2,p0,inverse,)
                p_list.append(p)
            return np.array(p_list)
        
        else:
            raise TypeError('type of p does not fit.')
            
def cal_miu3_ODE(miu1,miu2,x2, B=1):
    '''
    calculate miu_i+1 (miu3) via the ODE

    Parameters
    ----------
    miu1 : TYPE
        DESCRIPTION.
    miu2 : TYPE
        DESCRIPTION.
    x2 : TYPE
        DESCRIPTION.
    B : TYPE
        DESCRIPTION.

    Returns
    -------
    miu3 : TYPE
        DESCRIPTION.

    '''
    global e_charge
    # B= B * e_charge
    p2 = f_miu_p_1(miu2, inverse=True)
    miu3 = 2*miu2 - miu1 - B*(p2-x2)
    return miu3
    

def solve_miu_ODE(miu0, miu1, x_list):
    miu_list = np.zeros(len(x_list))
    miu_list[0]= miu0
    miu_list[1]= miu1
    i=1
    while i<= len(x_list)-2:
        miu_list[i+1]=cal_miu3_ODE(miu_list[i-1], miu_list[i], x_list[i])
        i+=1
    return miu_list
    
    
    

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
        x_list = np.array(x_list)
        return x_list
            
    else:
        raise TypeError('type of z does not fit.')
        

def f_xz_step(z, x0=0.4):
    if isinstance(z,(int, float, np.float64)):
        if z>=0:
            x = 0
        elif z<0:
            x = x0
        return x
    
    elif isinstance(z,(list, np.ndarray)):
        x_list=[]
        for i,zi in enumerate(z):
            x = f_xz_step(zi,x0)
            x_list.append(x)
        x_list = np.array(x_list)
        return x_list
            
    else:
        raise TypeError('type of z does not fit.')    
      
        
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
        

        
def funs(p1, x_i_list):
    miu_list = solve_miu_ODE(f_miu_p_1(x_i_list[0]),f_miu_p_1(p1), x_i_list)
    p_end = f_miu_p_1(miu_list[-1], inverse=True)
    return (p_end - x_i_list[-1])
    
    
def f(xx, b):
    return (xx**3 - b)
        
        
        
if __name__ == '__main__':
    
    e_charge= np.float64(1.602176634e-19)
    e_charge =1
    
    c = np.float64(1.2e-9)
    dz = c/2
    layer_index_list = f_layer_index_list(10,)
    z_i_list = f_z_layer(layer_index_list, dz)
    x_i_list = f_xz(z_i_list,)
    # miu_list = solve_miu_ODE(f_miu_p_1(0.4),f_miu_p_1(0.4), x_i_list)
    # p_list = f_miu_p_1(miu_list, inverse=True)
    
    sol = root_scalar(funs,args=(x_i_list), bracket=[0.3, 0.5], )
    p1 = sol.root
    miu_list = solve_miu_ODE(f_miu_p_1(0.4),f_miu_p_1(p1), x_i_list)
    p_list = f_miu_p_1(miu_list, inverse=True)
    
    
    
    # sol = root_scalar(f, args=(1), x0=0.2,x1=3)    
    
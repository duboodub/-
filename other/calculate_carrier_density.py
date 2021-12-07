# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 10:28:30 2021

@author: db
"""
import numpy as np
import matplotlib

if __name__ == '__main__':
    
    ## input a: , x[]:dopants density,  
    ## -> p[]: hole carrier density
    a=1
    x=np.array([1,1,0,0,1,1])
    xi= 0.45
    
    
    x = x*xi
    y = -a*x
    dim = len(x)
    A = np.eye(dim,k=1) + np.eye(dim,k=-1) - np.eye(dim)*(2+a)
    A[0,dim-1] = 1
    A[dim-1,0] = 1
    B = np.insert(A,dim,y,axis=1)
    p = np.linalg.solve(A,y)
    print(p)
    
    p_min = 0.07
    p_max = 0.2
    T_s = 9000
    # p[2]=0.165
    T_ph = (p_max - p[2])*(p[2]-p_min)*T_s
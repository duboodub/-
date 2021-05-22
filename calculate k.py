# -*- coding: utf-8 -*-
"""
Created on Sat May 22 01:09:16 2021

@author: db
"""

import pandas as pd
import numpy as np
import os

if __name__ == '__main__':
    excel_folder = ''
    excel_name = 'DB20210404m6,.xlsx'
    excel_path = os.path.join(excel_folder,excel_name)
    
    I1 = 20         #
    if I1 < 0:
        print('I1 should be >0 !')
    
    dI = 10         #
    I2 = I1 + dI
    # T=295K_(Scan H,2450)
    # Lakeshore643 Output/A
    # Resistance(Ω) (2450)

    # row = df1.index.get_indexer(df1[df1['Lakeshore643 Output/A'] == n1].index)
    # row1 = df1.index.get_loc(df1[df1['Lakeshore643 Output/A'] == n1].index[0])
    

    df2= pd.DataFrame(columns=['T/K','I(H)1+/A','R1+/Ohm', 'I(H)2+/A','R2+/Ohm', 'I(H)1-/A','R1-/Ohm', 'I(H)2-/A','R2-/Ohm', 'k(H>0)','k(H<0)','k(H>0) - k(H<0)'],index=[],)
    dict_df = {'T/K':pd.NA,'I(H)1+/A':pd.NA,'R1+/Ohm':pd.NA, 'I(H)2+/A':pd.NA,'R2+/Ohm':pd.NA, 'I(H)1-/A':pd.NA,
               'R1-/Ohm':pd.NA, 'I(H)2-/A':pd.NA,'R2-/Ohm':pd.NA,'k(H>0)':pd.NA, 'k(H<0)':pd.NA,'k(H>0) - k(H<0)':pd.NA}
    
    I_H_dict = {0:'I(H)1+/A', 1:'I(H)2+/A', 2:'I(H)1-/A', 3:'I(H)2-/A'}
    R_dict = { 0:'R1+/Ohm', 1:'R1-/Ohm', 2:'R2+/Ohm', 3:'R2-/Ohm'}
    
    T_list= np.arange(275,296,10)            #
    sheet_name_list = []
    for T in T_list:
        sheet_name = 'T=%dK_(Scan H,2450)'%(T)      #
        sheet_name_list.append(sheet_name)
        
    t = 0
    for sheet_name in sheet_name_list:
        T = T_list[t]
        t += 1
        
        df1 = pd.read_excel(excel_path, sheet_name=sheet_name, header=0,)
        
        r = list(range(4))
        r[0] = df1[df1['Lakeshore643 Output/A'] >= I1]['Lakeshore643 Output/A'].idxmin()
        r[1] = df1[df1['Lakeshore643 Output/A'] >= I2]['Lakeshore643 Output/A'].idxmin()
        r[2] = df1[df1['Lakeshore643 Output/A'] <= (-I1)]['Lakeshore643 Output/A'].idxmax()
        r[3] = df1[df1['Lakeshore643 Output/A'] <= (-I2)]['Lakeshore643 Output/A'].idxmax()
        
        col_I=df1.columns.get_loc('Lakeshore643 Output/A')
        col_R=df1.columns.get_loc('Resistance(Ω) (2450)')
        
        dict_df['T/K'] = T
        for i in range(len(r)):
            I_H = df1.iloc[r[i],col_I]
            R = df1.iloc[r[i],col_R]
            dict_df[I_H_dict[i]] = I_H
            dict_df[R_dict[i]] = R
            
            # df2.iloc[j,col_I] =  I_H
        df2 = df2.append(dict_df,True,)
    
    d11 = df2['R2+/Ohm']
    df2['k(H>0)'] = (df2['R2+/Ohm']-df2['R1+/Ohm']) / (df2['I(H)2+/A']-df2['I(H)1+/A'])
    df2['k(H<0)'] = (df2['R2-/Ohm']-df2['R1-/Ohm']) / (df2['I(H)2-/A']-df2['I(H)1-/A'])
    df2['k(H>0) - k(H<0)'] = df2['k(H>0)'] - df2['k(H<0)']
    
    dict2 = {'T':0,'I(H)1+/A':1,'k(H<0)':2,'k(H>0)':3,'k(H<0) - k(H>0)':4}
    dict3 = {'T':0,'Lakeshore643 Output/A':1,'k(H<0)':2,'k(H>0)':3,}
    # d4 = dict2['Lakeshore643 Output/A'] 
    # df2 = df2.append(dict2,True)
    # df2 = df2.append(dict3,True)
    
    
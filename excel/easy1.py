# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 03:59:00 2021

@author: db

input RHT excel book 

every es of T
    catch T
    creat es1, [R(Imin), R(Imax), mean(Imin), mean(Imax), std(Imin), std(), RH, RH_err,  ]
    


"""

import matplotlib.pyplot as plt 
import pandas as pd
from openpyxl import load_workbook, Workbook
import numpy as np
import os
from data_process_oop import Excel_Book, Excel_Sheet, File






if __name__ == '__main__':
    
    folder_path = r'F:\NAS-LAB-data\Data Temporary\Cryostat B\DUBO\DB20211101f1, LSMO0.67, RT, RHzT,\tdms\excel_copied_from_tdms\RHzT\meb\peb\2'
    file_name = 't=p, Switch-Slot1 CH2,t=m,.xlsx'
    file_name_RH_T = 'RH_T, '+ file_name
    
    eb = Excel_Book.load_excel_book(folder_path,file_name)
    
    eb1= Excel_Book(folder_path, file_name_RH_T)
    eb1.save()
    
    for sheet_name in eb.wb.sheetnames:
        if 'T=' in sheet_name:
            
            es = Excel_Sheet( eb, sheet_name = sheet_name)
            
            col_name_R = 'Resistance(Ω) '
            col_name_I = 'Lakeshore643 Output/A'
            
            df1 = pd.DataFrame(columns=['R(Imin)', 'R(Imax)', 'mean(Imin)', 'mean(Imax)', 'H(Imin)', 'H(Imax)', 'std(Imin)', 'std(Imax)', 'RH', 'RH_err', ])

            Is = {'Imin': -60, 'Imax': 60}
            for I in Is:
                
                df= es.df_es[es.df_es[col_name_I]==Is[I] ]
                H = df['H(from I)/Gauss'].iloc[0]
                
                df1['H(%s)'%I] = pd.Series([H])
                df1=df1.copy()
                df1['mean(%s)'%I] = pd.Series( [df['R(%s)'%I].mean()] )
                df1['std(%s)'%I] = pd.Series( [df['R(%s)'%I].std()] )
                df1['R(%s)'%I] = df[col_name_R]
                
            es1 = Excel_Sheet(data=df1, sheet_name=sheet_name, file= File(folder_path, file_name_RH_T))
            es1.save()
  
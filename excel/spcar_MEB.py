# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 04:32:13 2021

@author: db
"""

import matplotlib.pyplot as plt 
import pandas as pd
from openpyxl import load_workbook, Workbook
import numpy as np
import os

from data_process_oop import Excel_Book, Excel_Sheet, File

if __name__ == '__main__':
    # input
    folder_path = r'E:\NAS, data\Data Temporary\Cryostat A\dubo\DB20210728f1, sPCAR,Nb\excel_copied_from_tdms'
    folder_path_m = folder_path + r'\meb'           # measure books
    
    '''
    create meb
        input folder_path
        creat measure excel books of the excel books in the folder_path. concat all the columns.
        so far measure_type='RHT,switch'  only.
        
    '''
    file_name_list= os.listdir(folder_path)
    for file_name in file_name_list:
        if os.path.splitext(file_name)[1] == '.xlsx':
            print('creating measure excel book of {}'.format(file_name))
            eb = Excel_Book.load_excel_book(folder_path,file_name)
            
            I_SR830 = 6.1e5
            es = Excel_Sheet(eb,'spcar')
            es.df_es.insert(len(es.df_es.columns),'dV/dI (V/A)', I_SR830 *es.df_es['R SR830']/es.df_es['V SR830'],)
            es.df_es.insert(len(es.df_es.columns),'dI/dV (A/V)', 1/es.df_es['dV/dI (V/A)'],)
            es.df_es.insert(len(es.df_es.columns),'V/I (V/A)', es.df_es['voltage/V']/es.df_es['current/A'],)
            es.df_es.insert(len(es.df_es.columns),'I/V (A/V)', es.df_es['current/A']/es.df_es['voltage/V'],)
            es.save()
            print('created measure excel book of {}\n'.format(file_name))
            
            
            
            
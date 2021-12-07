# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 01:08:25 2021

@author: db
"""

'''
Input the folder_path, 
It will connect all the excel books with all sheets into the origin.

This example shows how to Customize the Excel data connector.
1. Parse headerlines to column labels.
2. Import partial cols and rows.
3. Specify the spreadsheet to import.
'''

from data_process_oop import Excel_Book, Excel_Sheet, File
import originpro as op
import os

#
folder_path = r'E:\NAS, data\Data Temporary\Cryostat B\DUBO\DB20210702f1, LSMO.5+33, RHxyT\excel_copied_from_tdms\RHT\meb\peb'
file_name_list = os.listdir(folder_path)
file_names = []
for file_name in file_name_list:
    if os.path.splitext(file_name)[1] == '.xlsx':
        file_names.append(file_name)
        
for file_name in file_names:
    eb = Excel_Book.load_excel_book(folder_path, file_name)
    f = eb.file.file_path
    #f = op.path('e')+r'Samples\Import and Export\Partial Import.xlsx'
    wks = op.new_sheet()

    #Create data connector object
    dc = op.Connector(wks, dctype='Excel', keep_DC=True)
    ss = dc.settings()

    #Headerlines to column label
    labels = ss['labels']
    labels[op.attrib_key('Use')] = '1'
    labels['longname'] = 1
    #labels['unit'] = 2

    '''
    #Setting for partial import
    partial = ss['partial']
    partial[op.attrib_key('Use')] = '1'
    partial['col'] = '1:3'
    partial['row'] = '1:99'
    '''
    
    for i, sheet_name in enumerate(eb.wb.sheetnames):
        if i == 0:
            dc.imp(f, sel= sheet_name )
        else:
            dc.new_sheet( sheet_name )


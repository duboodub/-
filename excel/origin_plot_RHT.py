import os
import originpro as op
import time
import numpy as np
from data_process_oop import Excel_Book, Excel_Sheet, File
import re

# Input three data files into three worksheets within one workbook
import originpro as op

def tryint(s):                       
    try:
        return int(s)
    except ValueError:
        return s

def str2int(v_str):                
    return [tryint(sub_str) for sub_str in re.split('([0-9]+)', v_str)]

def sort_humanly(v_list):   
    return sorted(v_list, key=str2int)

def sheet_names_from_Ts(temp_list):     
    sheet_name_list = []
    for T in temp_list:
        # sheet_name = 'T=%dK %s' %(T,sheet_name_original)
        #sheet_name = 'RH T=%dK 2450 only data_1'%T   # 2450 only
        #sheet_name = 'RH T=%dK_(Scan H,2450)'%T    # DB20210404m5,.xlsx
        sheet_name = 'T=%dK_(Scan H,2450)'%T    # DB20210404m5,.xlsx
        sheet_name_list.append(sheet_name)
        
    return sheet_name_list


    


def op_plot_RHT(WBook_name,WSheet_name_list,coly,colx):
    gl = op.new_graph(lname=WBook_name+', '+coly, template='RHT_line_py')[0]
    for wks_name in WSheet_name_list:
        wks = op.find_sheet('w','[%s]%s'%(WBook_name,wks_name))
        gl.add_plot(wks, coly=coly, colx=colx, type='line')
    gl.group(True)
    gl.rescale()
    
    return gl
        
    
def run_plot_RHT():
    wb_name = 'DB20210418m43,RxyHxyT1.xlsx'
    op.find_book('w','DB20210418m43,RxyHxyT1.xlsx')
    wb = op.find_book('w','DB20210418m43,RxyHxyT1.xlsx')

    #tempreture_list = np.arange(320, 9,10)
    tempreture_list = range(80,40,10)
    wks_name_list = sheet_names_from_Ts(tempreture_list)
    #coly = 'Resistance(Ω) (2450)'
    coly = 'R_f'
    colx = 'Lakeshore643 Output/A'
    
    op_plot_RHT(wb_name,wks_name_list,coly,colx)
    
    
    
if __name__ == '__main__':
    
    # just to get sheetnames
    folder_path = r'E:\NAS, data\Data Temporary\Cryostat B\DUBO\DB20210504f1\excel_copied_from_tdms\meb\peb'
    # creat wbook_name_list
    wbook_name_list = []
    file_list = os.listdir(folder_path)

    for wbook_name in file_list:
        if 'Switch-Slot' in wbook_name:      # identify book_name
            wbook_name_list.append(wbook_name)
    if wbook_name_list == []:
        raise ValueError('wbook_name_list == []')
    
    for wbook_name in wbook_name_list:
        print('\nplot of %s creating...'%wbook_name)
        eb = Excel_Book.load_excel_book(folder_path, wbook_name)
        
        # creat wks_name_list
        wks_name_list = []
        for wks_name in eb.wb.sheetnames:
            ic= wks_name[0:2]
            if ic == 'T=':
                wks_name_list.append(wks_name)
        if wks_name_list == []:
            raise ValueError('wks_name_list == []')
        wks_name_list = sort_humanly(wks_name_list)
        print('wks_name_list created.\n')
        
        # 记得在’sheet_names_from_Ts‘里修改sheetname格式
        # wb_name = 'bt=peb, Switch-Slot1 CH1,t=m,.xls'
        # wb = op.find_book('w',wb_name)
        
        #tempreture_list = np.arange(5, 86,10)
        #tempreture_list = np.append(tempreture_list, 5)
        #tempreture_list = range(30,60,10)
        #wks_name_list = sheet_names_from_Ts(tempreture_list)
        
        #coly = 'R_f'
        #coly = 'Resistance(Ω)'
        #coly = 'rho_sheet/Ohm'
        #coly = 'rho/(Ohm)cm'
        #coly = 'sample temperature/K'
        #colx = 'system time'
        
        colx = 'H(from I)/Gauss'
        coly_list = ['Resistance(Ω)','sample temperature/K','rho/(Ohm)cm', 'rho_sheet/Ohm']
        for coly in coly_list:
            op_plot_RHT(wbook_name, wks_name_list,coly,colx)
            print('plot <%s>-<%s> finished.'%(coly, colx))

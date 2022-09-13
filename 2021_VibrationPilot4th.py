import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import biomechanics_analysis as bio
from openpyxl import load_workbook

path = r'E:\EEG-NASA\ProjectV_Datatxt\2021_VibrationPilot4th_Data'
time = ['_pre', '_vib', '_post10', '_post20', '_follow10', '_follow20']
trial = ['_MVC', '_20MVC', '_30s']

os.chdir(path)
Sub = os.listdir()

Sub = [x for x in Sub if not x.endswith(".xlsx")]
        
#sub = 'Sub21'

for sub in Sub:
    os.chdir(sub)
    result_MVC = []
    result_20MVC = []
    result_acc1 = []
    result_acc2 = []
    result_std1 = []
    result_std2 = []
    #print(os.listdir())
    for t in time:
        #t = time[5]
        txtfile = bio.findtxt(t)
        list_remove = []
        count = 1
        for txt in txtfile:
            if '30-' in txt:
                list_remove.append(txt)
            if 'eeg' in txt:
                list_remove.append(txt)
        #print(list_remove)
        for remove in list_remove:
            txtfile.remove(remove)
        print(txtfile)
        list_acc = [0, 0]
        list_std = [0, 0]
        Data = {}
        for file in txtfile:
            #file = txtfile[1]
            Data[file] = pd.read_csv(file, delimiter='\t', names = ['Force', 'EMG', 'Trigger', 'Target'], index_col=False)
            #Check Data--------------------
            plt.plot(Data[file]['Force'])
            plt.plot(Data[file]['Trigger'], 'r')
            plt.title(file)
            plt.show()
            #plt.plot(Data[file]['EMG'])
            #plt.show()
            #------------------------------
            if '_MVC' in file:
                start = bio.forcestart(Data[file], 5)
                plt.plot(Data[file]['Force'])
                plt.plot(start, Data[file]['Force'][start], 'ro', mfc = 'None')
                plt.title(sub+' '+t+' MVC')
                plt.show()
                MVC = bio.mvccal(Data[file], start, 5)
            else:
                MVC = 0
            if '_20MVC' in file:
                trig_20MVC = bio.findtrig(Data[file])
                #del trig_20MVC[5]
                plt.plot(Data[file]['Force'])
                plt.plot(trig_20MVC, Data[file]['Force'][trig_20MVC], 'ro', mfc = 'None')
                plt.title(sub+' '+t+' 20MVC')
                plt.show()
                MVC20 = bio.mvc20cal(Data[file], trig_20MVC)
            if '_30' in file:
                trig_30s = bio.findtrig(Data[file])
                trig_30s[0] = int(trig_30s[0])
                plt.plot(Data[file]['Force'])
                plt.plot(trig_30s[0], Data[file]['Force'][trig_30s[0]], 'ro', mfc = 'None')
                plt.title(sub+' '+t+' 30-'+str(count))
                plt.show()
                acc = bio.accu(Data[file], trig_30s)
                std = bio.stab(Data[file], trig_30s)
                count+=1
                if '-1' in file:
                    list_acc[0] = acc
                    list_std[0] = std
                if '-2' in file:
                    list_acc[1] = acc
                    list_std[1] = std
        result_MVC.append(round(MVC, 2))
        result_20MVC.append(round(MVC20, 2))
        result_acc1.append(round(list_acc[0], 2))
        result_acc2.append(round(list_acc[1], 2))
        result_std1.append(round(list_std[0], 2))
        result_std2.append(round(list_std[1], 2))
    df = pd.DataFrame([result_MVC, result_20MVC, result_acc1, result_acc2, result_std1, result_std2], 
                  index = ['MVC', 'MVC20', 'acc1', 'acc2', 'std1', 'std2'], columns = time)
    book = load_workbook(r'E:\EEG-NASA\ProjectV_Datatxt\2021_VibrationPilot4th_Data\2021_VibrationPilot4th_2.xlsx')
    writer = pd.ExcelWriter(r'E:\EEG-NASA\ProjectV_Datatxt\2021_VibrationPilot4th_Data\2021_VibrationPilot4th_2.xlsx', engine = 'openpyxl')
    writer.book = book
    df.to_excel(writer, sheet_name = sub)
    writer.save()
    writer.close()
    os.chdir('..')
import os
import numpy as np
import pandas as pd

class test:
    def __init__(self, name, trial, mvc, mvc20, sta, acc):
        '''
        create a object to store ur results
        Parameters
        ----------
        name : TYPE: string
            DESCRIPTION: sub name
        trial : TYPE: string
            DESCRIPTION: trial name
        mvc : TYPE: float
            DESCRIPTION: mvc value
        mvc20 : TYPE: float
            DESCRIPTION: mvc20 value
        sta : TYPE: [float, float]
            DESCRIPTION: 30s stability values
        acc : TYPE: [float, float]
            DESCRIPTION: 30s accuracy values
        ----------
        '''
        self.name = name
        self.trial = trial
        self.mvc = mvc
        self.mvc20 = mvc20
        self.sta = sta
        self.acc = acc

def findtxt(name):
    '''
    find the txt file u want to analyze
    Parameters
    ----------
    name : TYPE: string
        DESCRIPTION: ur txt filename

    Returns
    -------
    temp_list : TYPE: list
        DESCRIPTION: file u need
    '''
    temp_list=[]
    filename = os.listdir()
    for ii in filename:
        if name in ii:
            temp_list.append(ii)
    print(temp_list)
    return temp_list

def forcestart(data, std_num):
    '''
    define when sub start to generate force and find that time point
    Parameters
    ----------
    data : TYPE: array
        DESCRIPTION: data u read
    std_num : TYPE: int
        DESCRIPTION: how many std u want to decide the start of generating force
    Returns
    temp3 : TYPE list
    -------
    '''
    #std_num = 20
    force = data['Force']
    mean = np.mean(force[500:1500])
    std = np.std(force[500:1500])
    threshold = mean + std_num * std
    force[force<threshold] = 0
    start = np.array(np.where(force > 0))
    temp = np.diff(start)
    temp1 = np.array(np.where(temp > 2))[1]+1
    temp1 = temp1.tolist()
    temp2 = start[0][temp1].tolist()
    temp3 = np.insert(temp2, 0 ,start[0][0]).tolist()
    return temp3

def mvccal(data, start, duration):
    '''
    calculate mvc
    Parameters
    ----------
    data : TYPE: array
        DESCRIPTION: data u want to calculate mvc
    start : TYPE: list
        DESCRIPTION: the time sub start to generate force
    duration : TYPE: int
        DESCRIPTION: how long sub generate force

    Returns
    mvc : TYPE: float
    -------
    '''
    duration = int(duration*1000)
    force = data['Force']
    temp_list=[]
    for i in start:
        temp = np.mean(force[i:i+duration])
        temp_list.append(temp)
    if len(temp_list)>3:
        #minimum = min(temp_list)
        del temp_list[temp_list.index(min(temp_list))]
    mvc = np.mean(temp_list)
    return mvc

def findtrig(data):
    '''
    find trigger pulse
    Parameters
    ----------
    data : TYPE: array
        DESCRIPTION: data u want find trigger time point
    mode : TYPE: int
        DESCRIPTION: 1 = 20MVC, 2 = 30s
    Returns
    -------
    '''
    trigger = data['Trigger']
    threshold = 4
    if max(trigger)<4:
        threshold = 3.5
    temp = np.where(trigger>threshold)
    temp2 = np.diff(temp)
    temp3 = np.array(np.where(temp2 > 2))[1]+1
    temp3 = temp3.tolist()
    temp4 = temp[0][temp3].tolist()
    temp4 = np.insert(temp4, 0 ,temp[0][0]).tolist()
    return temp4

def mvc20cal(data, trig_20MVC):
    '''
    calculate 20mvc
    Parameters
    ----------
    data : TYPE: array
        DESCRIPTION: the one u want to calculate 20mvc
    trig_20MVC : TYPE: list
        DESCRIPTION: file-20MVC trigger position
    Returns
    -------
    temp2 : TYPE
        DESCRIPTION.

    '''
    target = data['Target']
    temp = data['Force'][trig_20MVC]
    temp2 = np.mean(abs(temp-target))
    return temp2

def accu(data, trig_30s):
    '''
    calculate the stability of ur data
    Parameters
    ----------
    data : TYPE: array
        DESCRIPTION: data u want to calculate stability
    trig_30s : TYPE: list
        DESCRIPTION: file-30s trigger position
    Returns
    -------
    temp2 : TYPE: float
    '''
    target = data['Target']
    temp = data['Force'][trig_30s[0]:trig_30s[0]+30*1000]
    temp2 = np.sqrt(np.mean((temp-target)**2))
    return temp2

def stab(data, trig_30s):
    '''
    calculate the accuracy of ur data
    Parameters
    ----------
    data : TYPE: array
        DESCRIPTION: data u want to calculate accuracy
    trig_30s : TYPE: list
        DESCRIPTION: file-30s trigger position
    Returns
    -------
    temp2 : TYPE: float
    '''
    temp = data['Force'][trig_30s[0]:trig_30s[0]+30*1000]
    temp2 = np.std(temp)
    return temp2

def readexcel(filename, colnames):
    '''
    Read multiple sheet in Excel to a dict
    Parameters
    ----------
    filename : string
    colnames : string
    Returns :
    -------
    df :TYPE dict
    '''
    file = pd.ExcelFile('data4plot.xlsx')
    df = {}
    for i, name in enumerate(file.sheet_names):
        sheet = file.parse(name,header=1,names=colnames)
        df[name] = sheet
    file.close()
    return df
    
### Main script below--------------------------------------
# =============================================================================
# os.chdir(path)
# for i in sub:
#     os.chdir(i)    
#     txtfile = findtxt('_MVC')
#     #L = len(txtfile)
#     data_dict = {}
#     for j,k in zip(txtfile,range(len(txtfile))):
#         data_dict[j] = pd.read_csv(j, delimiter = '\t', names = ['force','trigger','target'], index_col=False)
#         data = data_dict[j].to_numpy().astype(float)
#         start = []
#         start = forcestart(data,40)
#         mvc = mvccal(data, start ,4.5)
#         print(j+' : '+str(mvc))
#         globals()[i+'_'+str(k)] = test(i,j,mvc,0,0,0)
#         
#         plt.plot(data[:,0])
#         plt.plot(start, data[:,0][start], 'ro', mfc='None')
#         plt.title(j)
#         plt.show()
#     
#     txtfile = findtxt('_20MVC')
#     data_dict = {}
#     for j in txtfile:
#         data_dict[j] = pd.read_csv(j, delimiter = '\t', names = ['force','trigger','target'], index_col=False)
#         data = data_dict[j].to_numpy().astype(float)
#         trig_20MVC = findtrig(data)
#         mvc20 = mvc20cal(data)
#         print(j+' : '+str(mvc20))
#         
#         plt.plot(data[:,0])
#         plt.plot(trig_20MVC, data[:,0][trig_20MVC], 'ro', mfc='None')
#         plt.title(j)
#         plt.show()
#         
#     txtfile = findtxt('30s')
#     data_dict = {}
#     for j in txtfile:
#         data_dict[j] = pd.read_csv(j, delimiter = '\t', names = ['force','trigger','target'], index_col=False)
#         data = data_dict[j].to_numpy().astype(float)
#         trig_30s = findtrig(data)
#         trig_30s[0] = int(trig_30s[0])
#         sta = stab(data)
#         acc = accu(data)
#         print(j+' stab : '+str(sta))
#         print(j+' accu : '+str(acc))
#         
#         trig_30s.insert(1, trig_30s[0]+30*force_hz)
#         plt.plot(data[:,0])
#         plt.plot(trig_30s, data[:,0][trig_30s],'ro', mfc='None')
#         plt.title(j)
#         plt.show()
#         
#     os.chdir('..')
# =============================================================================

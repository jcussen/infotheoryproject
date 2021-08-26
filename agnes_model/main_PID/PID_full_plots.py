import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *
from agnes_model.main_PID.PIDfuncs import PID_table, hebb_PID_table

#%% Import output data from model/matlab

hebbPath = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_Hebb/step_input/214568254_50.dat'
antiPath = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_antiHebb/step_input/832510732_50.dat'
scalPath = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_scaling/step_input/214568254_50.dat'

hebbData = get_firing_rates(read_data(hebbPath)) # load and read and process the data
antiData = get_firing_rates(read_data(antiPath)) # load and read and process the data
scalData = get_firing_rates(read_data(scalPath)) # load and read and process the data

#%% Run 4-variable PID analysis of data

hebb4dPID=hebb_PID_table(hebbData) #get 4 variable PID for the first condition!
anti4dPID=PID_table(antiData) #get 4 variable PID for the first condition!
scal4dPID=PID_table(scalData) #get 4 variable PID for the first condition!

PIDs4d=[hebb4dPID, anti4dPID, scal4dPID] # 214568254_50, 832510732_50, 214568254_50 are the seeds respectively!

#%% write to file!

file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/final_PIDs/reported_PIDs.pkl"

open_file = open(file_name, "wb")
pickle.dump(PIDs4d, open_file)
open_file.close()

# #%%SYNERGY PLOTS
#
# path_dic={1:'/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/PIDs/Hebb',
#           2:'/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/PIDs/anti',
#           3:'/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/PIDs/scal'}
#
# PIDs4d=[hebb4dPID, anti4dPID, scal4dPID]
#
# title_dic_4d={1: '2-Input PID Synergies for non-Preferred Pathway',
#            9:'2-Input PID Synergies for Preferred Pathway'}
#
# plastic_dic={1: ' (Hebbian)', 2: ' (Anti-Hebbian)', 3: ' (Homeostatic Scaling)'}
#
# pref_col_dic={'time':'Time', 'total_mi': "$I(X_{1}, X_{2}, X_{3}; T)$", 'redundancy': '$I_{\partial}^{\{1\} \{2\} \{3\}}$', 'ex_un': '$I_{\partial}^{\{1\}}$', 'synergy': '$I_{\partial}^{\{1 2 3\}}$'}
# nonpref_col_dic={'time':'Time', 'total_mi': "$I(Y_{1}, Y_{2}, Y_{3}; T)$", 'redundancy': '$I_{\partial}^{\{1\} \{2\} \{3\}}$', 'ex_un': '$I_{\partial}^{\{1\}}$', 'synergy': '$I_{\partial}^{\{1 2 3\}}$'}
# pref_dics={1: nonpref_col_dic, 9: pref_col_dic}
#
# def plot_PID(tb, pw, condition):
#     path=str(path_dic.get(condition))+'/new_PID_pw'+str(pw)
#     title=str(title_dic_4d.get(pw)) +str(plastic_dic.get(condition))
#     # print(filter_condition(tb, 1, pw).columns)
#     plot_table = filter_condition(tb, 1, pw).rename(columns=pref_dics.get(pw))
#     # cols=list(pref_dics.get(pw).values())
#     cols=['sy_12', 'sy_13']
#     # cols.remove('Time')
#     lines = plot_table.plot.line(title=title,style='.-', x='Time', y=cols ,color = ['yellow', 'goldenrod'])
#     lines.set_ylabel('Bits')
#     # lines.figure.savefig(path, bbox_inches="tight")
#     lines.figure.show()
#
# counting=1
# for table in PIDs4d:
#     plot_PID(table, 1, counting)
#     plot_PID(table, 9, counting)
#     counting += 1

#%% Get the plot table

path_dic={1:'/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/PIDs/Hebb',
          2:'/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/PIDs/anti',
          3:'/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/PIDs/scal'}

PIDs4d=[hebb4dPID, anti4dPID, scal4dPID]

title_dic_4d={1: 'PID Atoms for non-Preferred Pathway',
           9:'PID Atoms for Preferred Pathway'}

plastic_dic={1: ' (Hebbian)', 2: ' (Anti-Hebbian)', 3: ' (Homeostatic Scaling)'}

pref_col_dic={'time':'Time', 'total_mi': "$I(X_{1}, X_{2}, X_{3}; T)$", 'redundancy': '$I_{\partial}^{\{1\} \{2\} \{3\}}$', 'ex_un': '$I_{\partial}^{\{1\}}$', 'synergy': '$I_{\partial}^{\{1 2 3\}}$', 'sy_12': '$I_{\partial}^{\{1 2\}}*$', 'sy_13': '$I_{\partial}^{\{1 3\}}*$'}
nonpref_col_dic={'time':'Time', 'total_mi': "$I(Y_{1}, Y_{2}, Y_{3}; T)$", 'redundancy': '$I_{\partial}^{\{1\} \{2\} \{3\}}$', 'ex_un': '$I_{\partial}^{\{1\}}$', 'synergy': '$I_{\partial}^{\{1 2 3\}}$', 'sy_12': '$I_{\partial}^{\{1 2\}}*$', 'sy_13': '$I_{\partial}^{\{1 3\}}*$'}
pref_dics={1: nonpref_col_dic, 9: pref_col_dic}

def plot_PID(tb, pw, condition):
    path=str(path_dic.get(condition))+'/new_PID_pw'+str(pw)
    title=str(title_dic_4d.get(pw)) +str(plastic_dic.get(condition))
    # print(filter_condition(tb, 1, pw).columns)
    plot_table = filter_condition(tb, 1, pw).rename(columns=pref_dics.get(pw))
    cols=list(pref_dics.get(pw).values())
    cols.remove('Time')
    lines = plot_table.plot.line(style=['.-','-x','-o','-s','-*','-d'], x='Time', y=cols ,color = ['royalblue', 'red', 'forestgreen','purple', 'orange', 'yellow'])
    lines.set_ylabel('Bits')
    lines.figure.savefig(path, bbox_inches="tight")
    lines.figure.show()

counting=1
for table in PIDs4d:
    plot_PID(table, 1, counting)
    plot_PID(table, 9, counting)
    counting += 1

#%% Run 3-variable PID p1 off analysis of data

# hebbPID_p1off=p1off_PID_dataframe(hebbData) #get 4 variable PID for the first condition!
# antiPID_p1off=p1off_PID_dataframe(antiData) #get 4 variable PID for the first condition!
# scalPID_p1off=p1off_PID_dataframe(scalData) #get 4 variable PID for the first condition!

#%% Get the plot table

title_dic_p1off={1: 'PID Atoms for non-Preferred Pathway (Inhib. 1 Off)',
           9:'PID Atoms for Preferred Pathway (Inhib. 1 Off)'}

PIDs_p1off=[anti4dPID, scal4dPID]

# col_dic_p1off={'time':'Time', 'total_mi': "Mutual Information", 'redundancy': 'Redundancy', 'ex_un': 'Unique Excitatory', 'synergy': 'Synergy'}

pref_col_dic_p1off={'time':'Time','mi_13':'$I(X_{1}, X_{3}; T)$',
 'r_13':'$I_{\partial}^{\{1\} \{3\}}$',
 'un_13': '$I_{\partial}^{\{1\}}$',
 'sy_13': '$I_{\partial}^{\{1 3\}}$',
# 'mi_12': '$I(X_{1}, X_{2}; T)$',
# 'r_12': '$I_{\partial}^{\{1\} \{2\}}$',
#  'sy_12': '$I_{\partial}^{\{1 2\}}$',
#  'un_12': '$I_{\partial}^{\{1}}$',
#  'mi_23': '$I(X_{2}, X_{3}; T)$',
#  'r_23': '$I_{\partial}^{\{2\} \{3\}}$',
#  'sy_23': '$I_{\partial}^{\{2 3\}}$',
#  'un_23': '$I_{\partial}^{\{2\}}$'
               }

nonpref_col_dic_p1off={'time':'Time','mi_13':'$I(Y_{1}, Y_{3}; T)$',
 'r_13':'$I_{\partial}^{\{1\} \{3\}}$',
 'un_13': '$I_{\partial}^{\{1\}}$',
 'sy_13': '$I_{\partial}^{\{1 3\}}$',
# 'mi_12': '$I(X_{1}, X_{2}; T)$',
# 'r_12': '$I_{\partial}^{\{1\} \{2\}}$',
#  'sy_12': '$I_{\partial}^{\{1 2\}}$',
#  'un_12': '$I_{\partial}^{\{1}}$',
#  'mi_23': '$I(X_{2}, X_{3}; T)$',
#  'r_23': '$I_{\partial}^{\{2\} \{3\}}$',
#  'sy_23': '$I_{\partial}^{\{2 3\}}$',
#  'un_23': '$I_{\partial}^{\{2\}}$'
               }

pref_dics_p1off={1: nonpref_col_dic_p1off, 9: pref_col_dic_p1off}

def plot_PID_p1off(tb, pw, condition):
    path=str(path_dic.get(condition))+'/new_p1_off_pw'+str(pw)
    title=str(title_dic_p1off.get(pw))+str(plastic_dic.get(condition))
    # print(filter_condition(tb, 1, pw).columns)
    plot_table = filter_condition(tb, 2, pw).rename(columns=pref_dics_p1off.get(pw))
    cols=list(pref_dics_p1off.get(pw).values())
    cols.remove('Time')
    lines = plot_table.plot.line(style=['.-','-x','-o','-s'], x='Time', y=cols, color = ['royalblue', 'orangered', 'forestgreen','goldenrod'])
    lines.set_ylabel('Bits')
    lines.figure.savefig(path, bbox_inches="tight")
    lines.figure.show()

county=2
for table in PIDs_p1off:
    plot_PID_p1off(table, 1, county)
    plot_PID_p1off(table, 9, county)
    county += 1
#

#%% Get the plot table

title_dic_p2off={1: 'PID Atoms for non-Preferred Pathway (Inhib. 2 Off)',
           9:'PID Atoms for Preferred Pathway (Inhib. 2 Off)'}


PIDs_p2off=[anti4dPID, scal4dPID]

# col_dic_p1off={'time':'Time', 'total_mi': "Mutual Information", 'redundancy': 'Redundancy', 'ex_un': 'Unique Excitatory', 'synergy': 'Synergy'}
pref_col_dic_p2off={'time':'Time',
               # 'mi_13':'$I(X_{1}, X_{3}; T)$',
 # 'r_13':'$I_{\partial}^{\{1\} \{3\}}$',
 # 'sy_13': '$I_{\partial}^{\{1 3\}}$',
 # 'un_13': '$I_{\partial}^{\{1}}$',
'mi_12': '$I(X_{1}, X_{2}; T)$',
'r_12': '$I_{\partial}^{\{1\} \{2\}}$',
'un_12': '$I_{\partial}^{\{1\}}$',
'sy_12': '$I_{\partial}^{\{1 2\}}$',
#  'mi_23': '$I(X_{2}, X_{3}; T)$',
#  'r_23': '$I_{\partial}^{\{2\} \{3\}}$',
#  'sy_23': '$I_{\partial}^{\{2 3\}}$',
#  'un_23': '$I_{\partial}^{\{2\}}$'
               }

nonpref_col_dic_p2off={'time':'Time',
               # 'mi_13':'$I(X_{1}, X_{3}; T)$',
 # 'r_13':'$I_{\partial}^{\{1\} \{3\}}$',
 # 'sy_13': '$I_{\partial}^{\{1 3\}}$',
 # 'un_13': '$I_{\partial}^{\{1}}$',
'mi_12': '$I(Y_{1}, Y_{2}; T)$',
'r_12': '$I_{\partial}^{\{1\} \{2\}}$',
'un_12': '$I_{\partial}^{\{1\}}$',
'sy_12': '$I_{\partial}^{\{1 2\}}$',
#  'mi_23': '$I(X_{2}, X_{3}; T)$',
#  'r_23': '$I_{\partial}^{\{2\} \{3\}}$',
#  'sy_23': '$I_{\partial}^{\{2 3\}}$',
#  'un_23': '$I_{\partial}^{\{2\}}$'
               }

pref_dics_p2off={1: nonpref_col_dic_p2off, 9: pref_col_dic_p2off}

def plot_PID_p2off(tb, pw, condition):
    path=str(path_dic.get(condition))+'/new_p2_off_pw'+str(pw)
    title=str(title_dic_p2off.get(pw))+str(plastic_dic.get(condition))
    # print(filter_condition(tb, 1, pw).columns)
    plot_table = filter_condition(tb, 3, pw).rename(columns=pref_dics_p2off.get(pw))
    cols=list(pref_dics_p2off.get(pw).values())
    cols.remove('Time')
    lines = plot_table.plot.line(style=['.-','-x','-o','-s'], x='Time', y=cols, color = ['royalblue', 'orangered', 'forestgreen','goldenrod'])
    lines.set_ylabel('Bits')
    lines.figure.savefig(path, bbox_inches="tight")
    lines.figure.show()

cnt=2
for table in PIDs_p2off:
    plot_PID_p2off(table, 1, cnt)
    plot_PID_p2off(table, 9, cnt)
    cnt += 1
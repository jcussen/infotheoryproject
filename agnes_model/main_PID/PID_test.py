import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *
from agnes_model.main_PID.PIDfuncs import PID_table

#%% Import output data from model/matlab

hebbPath = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_Hebb/step_input/214568254_50.dat'
antiPath = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_antiHebb/step_input/832510732_50.dat'
scalPath = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_scaling/step_input/214568254_50.dat'

hebbData = get_firing_rates(read_data(hebbPath)) # load and read and process the data
antiData = get_firing_rates(read_data(antiPath)) # load and read and process the data
scalData = get_firing_rates(read_data(scalPath)) # load and read and process the data

# #%% Run 4-variable PID analysis of data
#
# hebb4dPID=full_PID_dataframe(hebbData) #get 4 variable PID for the first condition!
# anti4dPID=full_PID_dataframe(antiData) #get 4 variable PID for the first condition!
# scal4dPID=full_PID_dataframe(scalData) #get 4 variable PID for the first condition!
#
# #%% Get the plot table
#
# path_dic={1:'/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/PIDs/Hebb',
#           2:'/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/PIDs/anti',
#           3:'/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/PIDs/scal'}
#
# PIDs4d=[hebb4dPID, anti4dPID, scal4dPID]
#
# title_dic_4d={1: '3-Input PID for non-Preferred Pathway',
#            9:'3-Input PID for Preferred Pathway'}
#
# plastic_dic={1: ' (Hebbian)', 2: ' (Anti-Hebbian)', 3: ' (Homeostatic Scaling)'}
#
# col_dic={'time':'Time', 'total_mi': "Mutual Information", 'redundancy': 'Redundancy', 'ex_un': 'Unique Excitatory', 'synergy': 'Synergy'}
#
# def plot_PID(tb, pw, condition):
#     path=str(path_dic.get(condition))+'/3_input_pw'+str(pw)
#     title=str(title_dic_4d.get(pw)) +str(plastic_dic.get(condition))
#     # print(filter_condition(tb, 1, pw).columns)
#     plot_table = filter_condition(tb, 1, pw).rename(columns=col_dic)
#     lines = plot_table.plot.line(title=title, x='Time', y=["Mutual Information", 'Redundancy', 'Unique Excitatory', 'Synergy'],color = ['royalblue', 'orangered', 'forestgreen','goldenrod'])
#     lines.set_ylabel('Bits')
#     # lines.figure.savefig(path, bbox_inches="tight")
#     lines.figure.show()
#
# counting=1
# for table in PIDs4d:
#     plot_PID(table, 1, counting)
#     plot_PID(table, 9, counting)
#     counting += 1

#%% Get the big plot table
big_table=PID_table(hebbData)
scal_big_table=PID_table(scalData)
anti_big_table=PID_table(antiData)
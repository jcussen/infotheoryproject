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

hebb4dPID=full_PID_dataframe(hebbData) #get 4 variable PID for the first condition!
anti4dPID=full_PID_dataframe(antiData) #get 4 variable PID for the first condition!
scal4dPID=full_PID_dataframe(scalData) #get 4 variable PID for the first condition!

#%% Get the plot table

path_dic={1:'/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/PIDs/Hebb',
          2:'/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/PIDs/anti',
          3:'/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/PIDs/scal'}

PIDs4d=[hebb4dPID, anti4dPID, scal4dPID]

title_dic_4d={1: '3-Input PID for non-Preferred Pathway',
           9:'3-Input PID for Preferred Pathway'}

plastic_dic={1: ' (Hebbian)', 2: ' (Anti-Hebbian)', 3: ' (Homeostatic Scaling)'}

col_dic={'time':'Time', 'total_mi': "Mutual Information", 'redundancy': 'Redundancy', 'ex_un': 'Unique Excitatory', 'synergy': 'Synergy'}

def plot_PID(tb, pw, condition):
    path=str(path_dic.get(condition))+'/3_input_pw'+str(pw)
    title=str(title_dic_4d.get(pw)) +str(plastic_dic.get(condition))
    # print(filter_condition(tb, 1, pw).columns)
    plot_table = filter_condition(tb, 1, pw).rename(columns=col_dic)
    lines = plot_table.plot.line(title=title, x='Time', y=["Mutual Information", 'Redundancy', 'Unique Excitatory', 'Synergy'],color = ['royalblue', 'orangered', 'forestgreen','goldenrod'])
    lines.set_ylabel('Bits')
    lines.figure.savefig(path, bbox_inches="tight")
    lines.figure.show()

counting=1
for table in PIDs4d:
    plot_PID(table, 1, counting)
    plot_PID(table, 9, counting)
    counting += 1

#%% Run 3-variable PID p1 off analysis of data

hebbPID_p1off=p1off_PID_dataframe(hebbData) #get 4 variable PID for the first condition!
antiPID_p1off=p1off_PID_dataframe(antiData) #get 4 variable PID for the first condition!
scalPID_p1off=p1off_PID_dataframe(scalData) #get 4 variable PID for the first condition!

#%% Get the plot table

title_dic_p1off={1: '2-Input PID for non-Preferred Pathway (Pop. 1 Off)',
           9:'2-Input PID for Preferred Pathway (Pop. 1 Off)'}

PIDs_p1off=[antiPID_p1off, scalPID_p1off]

col_dic_p1off={'time':'Time', 'total_mi': "Mutual Information", 'redundancy': 'Redundancy', 'ex_un': 'Unique Excitatory', 'synergy': 'Synergy'}

def plot_PID_p1off(tb, pw, condition):
    path=str(path_dic.get(condition))+'/p1_off_pw'+str(pw)
    title=str(title_dic_p1off.get(pw))+str(plastic_dic.get(condition))
    # print(filter_condition(tb, 1, pw).columns)
    plot_table = filter_condition(tb, 2, pw).rename(columns=col_dic_p1off)
    lines = plot_table.plot.line(title=title, x='Time', y=["Mutual Information", 'Redundancy', 'Unique Excitatory', 'Synergy'],color = ['royalblue', 'orangered', 'forestgreen','goldenrod'])
    lines.set_ylabel('Bits')
    lines.figure.savefig(path, bbox_inches="tight")
    lines.figure.show()

county=2
for table in PIDs_p1off:
    plot_PID_p1off(table, 1, county)
    plot_PID_p1off(table, 9, county)
    county += 1

#%% Run 3-variable PID p2 off analysis of data

hebbPID_p2off=p2off_PID_dataframe(hebbData) #get 4 variable PID for the first condition!
antiPID_p2off=p2off_PID_dataframe(antiData) #get 4 variable PID for the first condition!
scalPID_p2off=p2off_PID_dataframe(scalData) #get 4 variable PID for the first condition!

#%% Get the plot table

title_dic_p2off={1: '2-Input PID for non-Preferred Pathway (Pop. 2 Off)',
           9:'2-Input PID for Preferred Pathway (Pop. 2 Off)'}

PIDs_p2off=[antiPID_p2off, scalPID_p2off]

col_dic_p2off={'time':'Time', 'total_mi': "Mutual Information", 'redundancy': 'Redundancy', 'ex_un': 'Unique Excitatory', 'synergy': 'Synergy'}

def plot_PID_p2off(tb, pw, condition):
    path=str(path_dic.get(condition))+'/p2_off_pw'+str(pw)
    title=str(title_dic_p2off.get(pw))+str(plastic_dic.get(condition))
    # print(filter_condition(tb, 1, pw).columns)
    plot_table = filter_condition(tb, 3, pw).rename(columns=col_dic_p2off)
    lines = plot_table.plot.line(title=title, x='Time', y=["Mutual Information", 'Redundancy', 'Unique Excitatory', 'Synergy'],color = ['royalblue', 'orangered', 'forestgreen','goldenrod'])
    lines.set_ylabel('Bits')
    lines.figure.savefig(path, bbox_inches="tight")
    lines.figure.show()

cnt=2
for table in PIDs_p2off:
    plot_PID_p2off(table, 1, cnt)
    plot_PID_p2off(table, 9, cnt)
    cnt += 1

#%% Get shuffled data and test significance:

def shuffle_data(data, sources, n_trials, n_conditions):
    surr=data.copy()
    for i in range(int(n_conditions)):
        for source in sources:
            pick_rows = np.array(list(range(n_trials))) + n_trials * i
            shuffled_vals = np.random.permutation(surr[source][pick_rows])
            surr[source][pick_rows]=shuffled_vals
    return surr

n_trials=50000
total_trials=hebbData.shape[0] # total number of observations
n_conditions=total_trials/n_trials # number of different experimental conditions
sources=['ex_spks_stim', 'in1_spks_stim', 'in2_spks_stim']

sur = shuffle_data(hebbData, sources, n_trials, n_conditions)
surr_pid = full_PID_dataframe(sur)

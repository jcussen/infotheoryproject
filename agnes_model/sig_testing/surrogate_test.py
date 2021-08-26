import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import time
import infotheory
from agnes_model.step_input.functions import *
from agnes_model.main_PID.PIDfuncs import PID_table, hebb_PID_table

#%% Import output data from model/matlab

# USE THE FULL DATAFRAMES!!! i.e. 50000 rows (for now)

hebbPath = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_Hebb/step_input/214568254_50.dat'
antiPath = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_antiHebb/step_input/832510732_50.dat'
scalPath = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_scaling/step_input/214568254_50.dat'

hebbData = get_firing_rates(read_data(hebbPath)) # load and read and process the data
antiData = get_firing_rates(read_data(antiPath)) # load and read and process the data
scalData = get_firing_rates(read_data(scalPath)) # load and read and process the data

# be careful here! The shuffling is not quite right for the anti-Hebbian condition as it has more observations

# #%% shuffle data params
#
# n_trials=50000 # number of trials per condition
# n_trials2=50000 # number of trials per condition
# new_trials=10000
# total_trials=hebbData.shape[0] # total number of observations
# n_conditions=total_trials/n_trials # number of different experimental conditions
# n_surrogates=1 # number of surrogate dataframes required
# surr_dfs=[] # list of surrogate dataframes
# sources=['ex_spks_stim', 'in1_spks_stim', 'in2_spks_stim']
#
# #%% make antiHebb shorter
# antiData['run']=np.floor((antiData['row_num'] % n_trials)/new_trials)+1 # create label for which simulation run the data is from
# antiData=antiData[antiData['run']==1]
# antiData=antiData.drop(columns='run') # drop run column
#
#%% shuffling function
def shuffle_data(data, sources, n_trials, n_conditions):
    surr=data.copy()
    for i in range(int(n_conditions)):
        for source in sources:
            pick_rows = np.array(list(range(n_trials))) + n_trials * i
            shuffled_vals = np.random.permutation(surr[source][pick_rows])
            surr[source][pick_rows]=shuffled_vals
    return surr

#%% orig PID
orig_hebb_PID=hebb_PID_table(hebbData)
orig_anti_PID=PID_table(antiData)
orig_scal_PID=PID_table(scalData)

#%% test PID of shuffled data
# shuff_hebb=shuffle_data(hebbData, ['ex_spks_stim', 'in1_spks_stim', 'in2_spks_stim'], 10000, hebbData.shape[0]/10000)

n_dfs=25
surr_PIDs=[[],[],[]]

t0 = time.time()
for i in range(n_dfs):
    shuff_hebb=shuffle_data(hebbData, ['ex_spks_stim', 'in1_spks_stim', 'in2_spks_stim'], 50000, hebbData.shape[0]/50000)
    shuff_hebb_PID=hebb_PID_table(shuff_hebb)
    shuff_anti=shuffle_data(antiData, ['ex_spks_stim', 'in1_spks_stim', 'in2_spks_stim'], 50000, antiData.shape[0]/50000)
    shuff_anti_PID=PID_table(shuff_anti)
    shuff_scal=shuffle_data(scalData, ['ex_spks_stim', 'in1_spks_stim', 'in2_spks_stim'], 50000, scalData.shape[0]/50000)
    shuff_scal_PID=PID_table(shuff_scal)
    surr_PIDs[0].append(shuff_hebb_PID)
    surr_PIDs[1].append(shuff_anti_PID)
    surr_PIDs[2].append(shuff_scal_PID)

file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/surrogate/25_surr_PIDs.pkl"

open_file = open(file_name, "wb")
pickle.dump(surr_PIDs, open_file)
open_file.close()

t1 = time.time()


total = t1-t0
print(total)
print('seconds')

# #%% create many surrogate data PIDs
# t0 = time.time()
#
# pids=[[],[],[]] # hebb, antihebb, scaling
#
# for i in range(5):
#     count=0
#     for data in [hebbData, antiData, scalData]:
#         sur=shuffle_data(data, sources, n_trials, n_conditions)
#         pid= PID_table(sur)
#         pids[count].append(pid)
#         count+=1
#
# file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/surrogate/10_final_PIDs.pkl"
#
# open_file = open(file_name, "wb")
# pickle.dump(pids, open_file)
# open_file.close()
#
# t1 = time.time()
#
# total = t1-t0
# print(total)
# print('seconds')
#
#%% check the pickle file that was created

open_file = open(file_name, "rb")
surrtest_PIDS = pickle.load(open_file)
open_file.close()

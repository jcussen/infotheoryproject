import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
import time
from agnes_model.step_input.functions import *

#%% Import output data from model/matlab

hebbPath = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_Hebb/step_input/214568254_50.dat'
antiPath = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_antiHebb/step_input/832510732_50.dat'
scalPath = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_scaling/step_input/214568254_50.dat'

hebbData = get_firing_rates(read_data(hebbPath)) # load and read and process the data
antiData = get_firing_rates(read_data(antiPath)) # load and read and process the data
scalData = get_firing_rates(read_data(scalPath)) # load and read and process the data

#%% Run 4-variable PID analysis of data

hebb2inputPID=PID_2way(hebbData) #get 4 variable PID for the first condition!
anti2inputPID=PID_2way(antiData) #get 4 variable PID for the first condition!
scal2inputPID=PID_2way(scalData) #get 4 variable PID for the first condition!


#%% Import list of data from pickle

n_trials=50000 # number of trials per condition
total_trials=hebbData.shape[0] # total number of observations
n_conditions=total_trials/n_trials # number of different experimental conditions
n_surrogates=5 # number of surrogate dataframes required
surr_dfs=[] # list of surrogate dataframes
sources=['ex_spks_stim', 'in1_spks_stim', 'in2_spks_stim']

#%% shuffling function

def shuffle_data(data, sources, n_trials, n_conditions):
    surr=data.copy()
    for i in range(int(n_conditions)):
        for source in sources:
            pick_rows = np.array(list(range(n_trials))) + n_trials * i
            shuffled_vals = np.random.permutation(surr[source][pick_rows])
            surr[source][pick_rows]=shuffled_vals
    return surr

shuff_hebb=shuffle_data(hebbData,sources, n_trials, n_conditions)

#%% shuffle and test again:

shuff_hebb_2input=PID_2way(shuff_hebb)

#%% shuffle others too

shuff_anti=shuffle_data(antiData,sources, n_trials, n_conditions)
shuff_scal=shuffle_data(scalData,sources, n_trials, n_conditions)

#%% test them
shuff_anti_2input=PID_2way(shuff_anti)
shuff_scal_2input=PID_2way(shuff_scal)

#%% create many surrogate data PIDs
import time
t0 = time.time()

pids=[[],[],[]] # hebb, antihebb, scaling

for i in range(1000):
    count=0
    for data in [hebbData, antiData, scalData]:
        sur=shuffle_data(data, sources, n_trials, n_conditions)
        pid= PID_2way(sur)
        pids[count].append(pid)
        count+=1

file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/surrogate/1000_3_inputPIDs.pkl"

open_file = open(file_name, "wb")
pickle.dump(pids, open_file)
open_file.close()

t1 = time.time()

total = t1-t0
print(total)
print('seconds')

#%% read in data

open_file = open(file_name, "rb")
_100PIDS = pickle.load(open_file)
open_file.close()


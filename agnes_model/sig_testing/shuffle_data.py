import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *

# #%% Import list of data from pickle
# file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_scaling/step_input/395401317_10.dat"
#
# open_file = open(file_name, "rb")
# data = pickle.load(open_file)
# open_file.close()
# # data=data[0]


#%% Import list of data from raw
file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_scaling/step_input/395401317_10.dat"

data=read_data(file_name) # read into pandas dataframe

#%% Import list of data from pickle

n_trials=10000 # number of trials per condition
total_trials=data.shape[0] # total number of observations
n_conditions=total_trials/n_trials # number of different experimental conditions
n_surrogates=5 # number of surrogate dataframes required
surr_dfs=[] # list of surrogate dataframes
sources=['ex_spks_stim', 'in1_spks_stim', 'in2_spks_stim']

#%% shuffling function
def shuffle_data(data):
    groups = [df for _, df in data.groupby(['subcondition', 'pathway', 'time'])]
    for group in groups:
        for source in sources:
            group[source]=group[source].sample(frac=1).reset_index(drop=True).values
    surr=pd.concat(groups).reset_index(drop=True)
    return surr

#%% perform shuffling - not THAT slow
for i in range(n_surrogates):
    surr_dfs.append(shuffle_data(data))

#%% get PIDs for shuffled dataframes- this is pretty slow...
# PID_shuff=[full_PID_dataframe(get_firing_rates(df)) for df in surr_dfs]


data=get_firing_rates(data)
test_surr=surr_dfs[0]
test_surr=get_firing_rates(test_surr)
# test_surr=test_surr.drop('run')

#%% get PID
PID_orig=p2off_PID_dataframe(data)

#%% get surrogate PIDs
surrPIDs=[]
surrPIDs_p1off=[]
surrPIDs_p2off=[]

for surr in surr_dfs:
    surrPIDs.append(full_PID_dataframe(test_surr))
    surrPIDs_p1off.append(p1off_PID_dataframe(test_surr))
    surrPIDs_p2off.append(p2off_PID_dataframe(test_surr))

#%% output surrogate PIDs




import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *

#%% Import list of data from pickle
file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/Hebb_antiHebb/832510732_full.pkl"

open_file = open(file_name, "rb")
data = pickle.load(open_file)
open_file.close()

#%% Import list of data from pickle

n_trials=50000 # number of trials per condition
total_trials=data.shape[0] # total number of observations
n_conditions=total_trials/n_trials # number of different experimental conditions
n_surrogates=4 # number of surrogate dataframes required
surr_dfs=[] # list of surrogate dataframes
sources=['ex_spks_stim', 'in1_spks_stim', 'in2_spks_stim']

#%% perform shuffling - not THAT slow
for i in range(n_surrogates):
    surr=data
    for i in range(int(n_conditions)):
        for source in sources:
            surr.loc[i*n_trials:(i+1)*n_trials,source]=surr.loc[i*n_trials:(i+1)*n_trials,source].sample(frac=1).reset_index(drop=True).values
    surr_dfs.append(surr)

#%% get PIDs for shuffled dataframes- this is pretty slow...
PID_shuff=[full_PID_dataframe(get_firing_rates(df)) for df in surr_dfs]

#%% get PIDs for shuffled dataframes- this is quite slow


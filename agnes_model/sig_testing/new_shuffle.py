import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *

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

def shuffle_data(data, sources, n_trials, n_conditions):
    surr=data.copy()
    for i in range(int(n_conditions)):
        for source in sources:
            pick_rows = np.array(list(range(n_trials))) + n_trials * i
            shuffled_vals = np.random.permutation(surr[source][pick_rows])
            surr[source][pick_rows]=shuffled_vals
    return surr

surr_ex=shuffle_data(data, sources)

#%% check shuffling does what you think it does: IT DOES!
orig_test=data.loc[50000:59999, 'ex_spks_stim']
shuff_test=surr_ex.loc[50000:59999, 'ex_spks_stim']

# all= pd.Series(pd.concat([orig_test, shuff_test]))

orig_test_sorted=orig_test.value_counts().sort_index()
shuff_test_sorted=shuff_test.value_counts().sort_index()

shuff_concat = pd.concat([orig_test, shuff_test], axis=1)

orig_test.equals(shuff_test)
orig_test_sorted.equals(shuff_test_sorted)


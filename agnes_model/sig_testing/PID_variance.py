import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *

#%% Import list of data from pickle
file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/Hebb_antiHebb/832510732.pkl"

open_file = open(file_name, "rb")
runs = pickle.load(open_file)
open_file.close()

#%% Import list of data from pickle

PID_runs=[full_PID_dataframe(get_firing_rates(df)) for df in runs]

#%% Concat and calculate mean and std/var of atoms

df_PID = pd.concat(PID_runs).groupby(['subcondition','pathway', 'time']).agg(['mean', 'var'])

# Here we can see that the variance is very small across all the dataframes, the standard deviation is larger.
# Results seem to be fairly consistent


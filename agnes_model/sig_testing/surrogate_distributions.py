# THIS FILE COMPARES THE OUR PID VALUES TO SURROGATE ONES AND DETERMINES STATISTICAL SIGNIFICANCE I.E. TESTS NULL HYPOTHESIS
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *
from agnes_model.main_PID.PIDfuncs import *

#%% Import list of data from pickle
file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/surrogate/75_surr_PIDs.pkl"

open_file = open(file_name, "rb")
surrs = pickle.load(open_file)
open_file.close()

#%% Import list of data from pickle

hebb_PIDs=surrs[0]
anti_PIDs= surrs[1]
scal_PIDs= surrs[2]

#%%
n=75

mean_hebb = pd.concat(hebb_PIDs).groupby(['subcondition','pathway', 'time']).mean().reset_index()
std_hebb = pd.concat(hebb_PIDs).groupby(['subcondition','pathway', 'time']).std().reset_index()

mean_anti = pd.concat(anti_PIDs).groupby(['subcondition','pathway', 'time']).mean().reset_index()
std_anti = pd.concat(anti_PIDs).groupby(['subcondition','pathway', 'time']).std().reset_index()

mean_scal = pd.concat(scal_PIDs).groupby(['subcondition','pathway', 'time']).mean().reset_index()
std_scal = pd.concat(scal_PIDs).groupby(['subcondition','pathway', 'time']).std().reset_index()

#%%
n=75



import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *
# from agnes_model.step_input.parameters import *

#%% Import output data from model/matlab


large_data_path= '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_antiHebb/step_input/832510732_50.dat'
data=read_data(large_data_path) # read into pandas dataframe

#%% Export to pickle

file_name_full = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/Hebb_antiHebb/832510732_full.pkl"
# comment/uncomment this when needed! Write to pickle file!
open_file = open(file_name_full, "wb")
pickle.dump(data, open_file)
open_file.close()

#%% split table into 5 separate sets of observations

n_trials=50000 # number of trials
new_trials=10000

data['run']=np.floor((data['row_num'] % n_trials)/new_trials)+1 # create label for which simulation run the data is from

#%% create list of new 5 tables of observations

runs=[data[data['run']==i] for i in [1,2,3,4,5]]
for table in runs:
    table=table.drop(columns='run') # drop run column

#%% output and save as pickle object

file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/Hebb_antiHebb/832510732.pkl"

# comment/uncomment this when needed! Write to pickle file!
open_file = open(file_name, "wb")
pickle.dump(runs, open_file)
open_file.close()




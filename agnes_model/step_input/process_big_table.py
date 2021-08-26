import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *
# from agnes_model.step_input.parameters import *

#%% Import output data from model/matlab

# Hebbian data paths
hebb_1='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_Hebb/step_input/214568254_50.dat'
hebb_2='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_Hebb/step_input/561825436_50.dat'

# anti-Hebbian paths
anti_1='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_antiHebb/step_input/832510732_50.dat'
anti_2='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_antiHebb/step_input/561825436_50.dat'

# homeostatic scaling paths
scal_1='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_scaling/step_input/214568254_50.dat'
scal_2='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_scaling/step_input/561825436_50.dat'

# large_data_path= '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_antiHebb/step_input/832510732_50.dat'
hebb_1=read_data(hebb_1) # read into pandas dataframe
hebb_2=read_data(hebb_2) # read into pandas dataframe

anti_1=read_data(anti_1) # read into pandas dataframe
anti_2=read_data(anti_2) # read into pandas dataframe

scal_1=read_data(scal_1) # read into pandas dataframe
scal_2=read_data(scal_2) # read into pandas dataframe


# #%% Export to pickle
#
# file_name_full = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/Hebb_antiHebb/832510732_full.pkl"
# # comment/uncomment this when needed! Write to pickle file!
# open_file = open(file_name_full, "wb")
# pickle.dump(data, open_file)
# open_file.close()

#%% split table into 5 separate sets of observations

n_trials=50000 # number of trials
new_trials=10000

def sep_tables(data, n_trials, new_trials): # create smaller sets of observations
    data['run']=np.floor((data['row_num'] % n_trials)/new_trials)+1 # create label for which simulation run the data is from
    runs=[data[data['run']==i] for i in [1,2,3,4,5]]
    for table in runs:
        table=table.drop(columns='run') # drop run column
    return runs


def process_all(listo, n_trials, new_trials):
    output=[]
    for data in listo:
        sep_data=sep_tables(data, n_trials, new_trials)
        output.append(sep_data)
    return output




#%% output and save as pickle object


all_data= process_all([hebb_1, hebb_2, anti_1, anti_2, scal_1, scal_2], 50000, 10000)

file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/all_variance.pkl"

# comment/uncomment this when needed! Write to pickle file!
open_file = open(file_name, "wb")
pickle.dump(all_data, open_file)
open_file.close()




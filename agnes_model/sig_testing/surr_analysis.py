import pickle
import pandas as pd
import numpy as np

#%% import the data from pickle
file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/surrogate/75_surr_PIDs.pkl"

open_file = open(file_name, "rb")
surr_PIDs = pickle.load(open_file)
open_file.close()

#%% concat the dataframes
hebb_surr= pd.concat(surr_PIDs[0])
anti_surr= pd.concat(surr_PIDs[1])
scal_surr= pd.concat(surr_PIDs[2])

#%% group by and get mean, variance, max values

hebb_max=hebb_surr.groupby(['subcondition','pathway', 'time']).agg(['max'])
hebb_mean=hebb_surr.groupby(['subcondition','pathway', 'time']).agg(['mean'])

anti_max=anti_surr.groupby(['subcondition','pathway', 'time']).agg(['max'])
anti_mean=anti_surr.groupby(['subcondition','pathway', 'time']).agg(['mean'])

scal_max=anti_surr.groupby(['subcondition','pathway', 'time']).agg(['max'])
scal_mean=anti_surr.groupby(['subcondition','pathway', 'time']).agg(['mean'])

#%% compare with final PID results tables! do indicator table showing if result is significant!

file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/final_PIDs/reported_PIDs.pkl"

open_file = open(file_name, "rb")
final_PIDs = pickle.load(open_file)
open_file.close()

#%% unpack pickle file

hebb_final=final_PIDs[0]
anti_final=final_PIDs[1].drop(columns=['un_31', 'un_21', 'un_32'])
scal_final=final_PIDs[2].drop(columns=['un_31', 'un_21', 'un_32'])

#%% reset indices
hebb_max=hebb_max.reset_index()
anti_max=anti_max.reset_index()
scal_max=scal_max.reset_index()

#%% get difference between dataframes
hebb_sig=hebb_final-hebb_max.values
anti_sig=anti_final-anti_max.values
scal_sig=scal_final-scal_max.values

#create binary truth tables for significance
# hebb_sig[hebb_sig>=0]=1
# hebb_sig[hebb_sig<0]=0
# anti_sig[anti_sig>=0]=1
# anti_sig[anti_sig<0]=0
# scal_sig[scal_sig>=0]=1
# scal_sig[scal_sig<0]=0


hebb_sig[['subcondition', 'pathway', 'time']]=hebb_final[['subcondition', 'pathway', 'time']]
anti_sig[['subcondition', 'pathway', 'time']]=anti_final[['subcondition', 'pathway', 'time']]
scal_sig[['subcondition', 'pathway', 'time']]=scal_final[['subcondition', 'pathway', 'time']]

#%% get difference between dataframes
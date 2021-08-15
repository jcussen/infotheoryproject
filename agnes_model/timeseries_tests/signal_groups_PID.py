import numpy as np
import matplotlib.pyplot as plt
from dit.pid import *
import pandas as pd
import scipy.io
import h5py
import pickle
import matplotlib
import dit
from dit.inference import binned, dist_from_timeseries
from dit.multivariate import total_correlation as I, intrinsic_total_correlation as IMI # this is why these abbreviations are not in the functions!
from dit.pid.helpers import compare_measures
from dit.pid.distributions import bivariates, trivariates
dit.ditParams['print.exact'] = dit.ditParams['repr.print'] = True
dit.ditParams['text.font'] = 'linechar'

#%% Import spiking data from model
ex_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/AgnesModel/matlab_analysis/ex_output.pkl'
in1_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/AgnesModel/matlab_analysis/in1_output.pkl'
in2_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/AgnesModel/matlab_analysis/in2_output.pkl'
post_path = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/AgnesModel/matlab_analysis/post_output.pkl'

with open(ex_path, 'rb') as fin :
    ex = pickle.load(fin)
with open(in1_path, 'rb') as fin :
    in1 = pickle.load(fin)
with open(in2_path, 'rb') as fin :
    in2 = pickle.load(fin)
with open(post_path, 'rb') as fin :
    post = pickle.load(fin)

post[post>0]=1 # fix and binarise the sequence
post=np.reshape(post, (post.shape[1]))


#%% Model params
channels= 16
sample_rate_ms= 5

samples_per_sec= 1000/sample_rate_ms
rows=ex.shape[0]
total_time_secs= rows/samples_per_sec


#%% binning and PID params
TRANSIENTS = 1000
ITERATIONS = 1000000
BINS = 2
HISTORY_LENGTH = 1

#%% selecting the channels that we want to use

ex_ch9= ex[:, 8]
in1_ch9= in1[:, 8]
in2_ch9= in2[:, 8]

#%% maximum entropy binning of the data - discretization
ex_time_series = binned(ex_ch9, bins=BINS)
in1_time_series = binned(in1_ch9, bins=BINS)
in2_time_series = binned(in2_ch9, bins=BINS)
post_time_series= post # binary output?

post_agg=pd.Series(post_time_series).rolling(8).max().shift(periods=-8).fillna(0) # aggregated time series

#%% concat all activity vectors into one table
full_timeseries=np.transpose(np.vstack((ex_time_series, in1_time_series, post_agg)))

#in2_time_series,
#%% create the dit distribution object
time_series_distribution = dist_from_timeseries(full_timeseries, history_length=0)


#%%
PID_dep(time_series_distribution)

import numpy as np
import matplotlib.pyplot as plt
from dit.pid import *
import scipy.io
import pandas as pd
import matplotlib
import dit
from dit.inference import binned, dist_from_timeseries
from dit.multivariate import total_correlation as I, intrinsic_total_correlation as IMI # this is why these abbreviations are not in the functions!
from dit.pid.helpers import compare_measures
from dit.pid.distributions import bivariates, trivariates
dit.ditParams['print.exact'] = dit.ditParams['repr.print'] = True
dit.ditParams['text.font'] = 'linechar'

#%% Import spiking data from model
ex_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_Hebb/contrl/ex_activity.dat'
in1_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_Hebb/contrl/in1_activity.dat'
in2_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_Hebb/contrl/in2_activity.dat'
post_path = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_Hebb/contrl/post_activity.dat'

ex = np.loadtxt(ex_path)
in1 = np.loadtxt(in1_path)
in2 = np.loadtxt(in2_path)
post = np.loadtxt(post_path)

#%% Model params
channels= 16
sample_rate_ms= 10

samples_per_sec= 1000/sample_rate_ms
rows=ex.shape[0]/channels
total_time_secs= rows/samples_per_sec

#%% Reshape the data
ex = np.reshape(ex, (int(rows), channels), order='F')
in1 = np.reshape(in1, (int(rows), channels), order='F')
in2 = np.reshape(in2, (int(rows), channels), order='F')

#%% calculate average activity across all channels
av_ex= np.mean(ex, axis=1)
av_in1= np.mean(in1, axis=1)
av_in2= np.mean(in2, axis=1)

#%% plot activity
time= np.arange(start=0, stop=av_ex.shape[0], step=1) # simple time variable for plots
plt.figure(1)
plt.plot(time, av_in2)
plt.show()

#%% binning and PID params
TRANSIENTS = 1000
ITERATIONS = 1000000
BINS = 4
HISTORY_LENGTH = 1

#%% maximum entropy binning of the data - discretization
av_ex_time_series = binned(av_ex, bins=BINS)
av_in1_time_series = binned(av_in1, bins=BINS)
av_in2_time_series = binned(av_in2, bins=BINS)
post_time_series= binned(post, bins=2) # binary output?

#%% concat all activity vectors into one table
full_timeseries=np.transpose(np.vstack((av_ex_time_series, av_in1_time_series, av_in2_time_series, post_time_series)))

#%% create the dit distribution object
time_series_distribution = dist_from_timeseries(full_timeseries, history_length=0)

#%% explore the dit distribution object
print(time_series_distribution)

#%% Run PID measure on the distribution:
PID_BROJA(time_series_distribution) # taking ages to run?

#%% Bivariate PID


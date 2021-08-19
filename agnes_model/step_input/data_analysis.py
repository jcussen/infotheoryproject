import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *
from agnes_model.step_input.parameters import *

#%% Import output data from model/matlab

# seed1path= '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/copyagnes/flexible_switch_new2/step_input/output/Hebbian_scaling/scal_all.dat'
seed0path = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_scaling/step_input/395401317_10.dat'
# data1 = np.loadtxt(full_path) # this works quite quickly!
# data2 = np.loadtxt(path2) # this works quite quickly!

#%% Fully read the data into pandas

seed0=read_data(seed0path)
# seed1=read_data(seed1path)

#%% Calculate actual firing rates for data

seed0=get_firing_rates(seed0)
# seed1=get_firing_rates(seed1)



#%% Run PID analysis of data - This is the Hebbian scaling condition!!!

# data_201=pid_cols(filter_data(data, 2, 1, 0)) # subcondition k=1,2,3, time=0,1,2,5,10,20

df0=full_PID_dataframe(seed0)
# df1=full_PID_dataframe(seed1)


# df2=full_PID_dataframe(data2)


#%% Get the plot table

plot_table=filter_condition(df0, 1, 1)

#%% Plot the data!

lines=plot_table.plot.line(x='time', y=['total_mi','redundancy', 'ex_un', 'synergy'])
lines.figure.show()

#%% Get the plot table 2

plot_table2=filter_condition(df0, 3, 1)

#%% Plot the data 2!

lines2=plot_table2.plot.line(x='time', y=['total_mi','redundancy', 'ex_un', 'synergy'])
lines2.figure.show()



#%% Notes

# data_cond3=pid_cols(filter_data(data, 3, 1, 20))

# KEY POINT: the reason why there is no mutual information in the final simulation subcondition (i.e. population 2 off)
# is because there are very few postsynaptic spikes - the inhibition is too strongly connected!

# KEY IDEA: need to also plot and calculate the full mutual information alongside PID atoms to see how this influences their values.



import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.pulsemodelling.functions import *

#%% Import output data from model/matlab

full_path = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/AgnesModel/matlab_analysis/bigdata/all.dat'
data = np.loadtxt(full_path) # this works quite quickly!

#%% Run PID analysis of data - This is the Hebbian scaling condition!!!

data_201=pid_cols(filter_data(data, 2, 1, 0)) # subcondition k=1,2,3, time=0,1,2,5,10,20

# create empty dataframe
df = pd.DataFrame(columns=['subcondition', 'pathway', 'time', 'total_mi', 'ex_un', 'in1_un', 'in2_un', 'redundancy', 'synergy'])

for k in [1,2,3]:
    for pw in [1, 9]:
        for t in [0,1,2,5,10,20]:
            dat= pid_cols(filter_data(data, k, pw, t))
            mi, u1, u2, u3, r, sy = get_pid_4D(dat)
            df = df.append({'subcondition': k,
                            'pathway': pw,
                            'time': t,
                            'total_mi': mi,
                            'ex_un': u1,
                            'in1_un': u2,
                            'in2_un': u3,
                            'redundancy': r,
                            'synergy': sy}, ignore_index=True)


#%% Check the filtered data

data_cond3=pid_cols(filter_data(data, 3, 1, 20))

# KEY POINT: the reason why there is no mutual information in the final simulation subcondition (i.e. population 2 off)
# is because there are very few postsynaptic spikes - the inhibition is too strongly connected!

# KEY IDEA: need to also plot and calculate the full mutual information alongside PID atoms to see how this influences their values.



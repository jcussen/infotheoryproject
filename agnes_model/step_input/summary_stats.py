import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *
# from agnes_model.step_input.parameters import *

#%% Import output data from model/matlab

file_path= '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_scaling/step_input/832510732_10.dat'

#%% read the data into pandas

data=read_data(file_path)

#%% group by to create summary stats

agg_dict={'step_firrate': ['mean','std'],
          'postsynaptic_spks': ['mean','std'],
         'ex_spks_total': ['mean','std'],
         'in1_spks_total': ['mean','std'],
         'in2_spks_total': ['mean','std'],
         'ex_spks_stim': ['mean','std'],
         'in1_spks_stim': ['mean','std'],
         'in2_spks_stim': ['mean','std']}

summary_stats=data.groupby(['subcondition', 'pathway', 'time']).mean()
summary_stats=summary_stats.drop(columns='row_num')
summary_stats=summary_stats.add_suffix('_mean')

#%% join with other tables


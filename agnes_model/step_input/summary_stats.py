import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *
from agnes_model.step_input.parameters import *

#%% Import output data from model/matlab

seed1path= '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/copyagnes/flexible_switch_new2/step_input/output/Hebbian_scaling/scal_all.dat'
seed0path = '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_scaling/scaling_seed0.dat'
# data1 = np.loadtxt(full_path) # this works quite quickly!
# data2 = np.loadtxt(path2) # this works quite quickly!

#%% Fully read the data into pandas

seed0=read_data(seed0path)
seed1=read_data(seed1path)
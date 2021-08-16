import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *
# from agnes_model.step_input.parameters import *

#%% Import output data from model/matlab

#filepaths
hebb_hebb_time_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_Hebb/learning/data03.dat'
hebb_anti_time_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_antiHebb/learning/data03.dat'
hebb_scal_time_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_scaling/learning/data03.dat'


#read in data
hebb_hebb_time_wts = np.loadtxt(hebb_hebb_time_path)
hebb_anti_time_wts = np.loadtxt(hebb_anti_time_path)
hebb_scal_time_wts = np.loadtxt(hebb_scal_time_path)

#%% Import output data from model/matlab
def process_data(dat):
    dat[:, 0]=dat[:, 0]/1000 # convert milliseconds to seconds
    return dat

def plot_data(dat):
    pop1= dat[:, 0:17]
    pop2=dat[:, np.r_[0,17:33]]
    pop1 = pd.DataFrame(data=pop1)
    pop2 = pd.DataFrame(data=pop2)
    output1=pop1.set_index(0).plot(title='Inhibitory Population 1 av weights by signal group')
    output1.figure.show()
    output2=pop2.set_index(0).plot(title='Inhibitory Population 2 av weights by signal group')
    output2.figure.show()


alldata=[hebb_hebb_time_wts, hebb_anti_time_wts, hebb_scal_time_wts]

for data in alldata:
    dat=process_data(data)
    plot_data(dat)





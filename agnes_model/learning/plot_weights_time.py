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
    dat[:, 0]=dat[:, 0]/60000 # convert milliseconds to minutes
    return dat

def plot_data(dat, output_folder_path):
    pop1= dat[:, 0:17]
    pop2=dat[:, np.r_[0,17:33]]
    pop1 = pd.DataFrame(data=pop1)
    pop2 = pd.DataFrame(data=pop2)
    output1=pop1.set_index(0).plot()
    output1.set_xlabel('Time (mins)')
    output1.set_ylabel('Mean Weight')
    output1.legend(bbox_to_anchor=(1.0, 1.0), borderpad=0.5)
    output1.legend(title='Signal group', bbox_to_anchor=(1.0, 1.0), borderpad=0.5)
    output1_path=str(output_folder_path)+'/new_pop1.png'
    output1.figure.savefig(output1_path, bbox_inches="tight")
    output1.figure.show()
    output2=pop2.set_index(0).plot()
    output2.legend(title='Signal group',bbox_to_anchor=(1.0, 1.0), borderpad=0.5)
    output2.set_xlabel('Time (mins)')
    output2.set_ylabel('Mean Weight')
    output2_path = str(output_folder_path)+'/new_pop2.png'
    output2.figure.savefig(output2_path, bbox_inches="tight")
    output2.figure.show()


heb_fig_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/learning/Hebb'
anti_fig_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/learning/anti'
scal_fig_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/learning/scal'


alldata=[hebb_hebb_time_wts, hebb_anti_time_wts, hebb_scal_time_wts]

# PLOT all the data
plot_data(process_data(alldata[0]), heb_fig_path)
plot_data(process_data(alldata[1]), anti_fig_path)
plot_data(process_data(alldata[2]), scal_fig_path)




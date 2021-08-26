import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *
# from agnes_model.step_input.parameters import *

#filepaths
hebb_hebb_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_Hebb/learning/sampled_weights.dat'
hebb_anti_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_antiHebb/learning/sampled_weights.dat'
hebb_scal_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/data/Hebb_scaling/learning/sampled_weights.dat'


#read in data
hebb_hebb_wts = np.loadtxt(hebb_hebb_path)
hebb_anti_wts = np.loadtxt(hebb_anti_path)
hebb_scal_wts = np.loadtxt(hebb_scal_path)

#%% Import output data from model/matlab
def process_data(dat, time_point):
    dat=dat[:, np.r_[0, time_point]] # get final state of the weights
    ex=dat[0:3200, :]
    in1 = dat[3200:3600, :]
    in2 = dat[3600:4000, :]
    ex[:, 0]=(ex[:,0]/200)
    in1[:,0]= ((in1[:,0]-3200)/400)*(3200/200)
    in2[:,0] = ((in2[:,0]-3600)/400) * (3200/200)
    return ex, in1, in2


col_dic= {1:'orangered',
          2: 'darkblue',
          3: 'dodgerblue'}

pop_dic= {1:'Excitatory Pop.',
          2: 'Inhibitory Pop. 1',
          3: 'Inhibitory Pop. 2'}

title_dic_bef= {1:'Hebbian Control Condition Weight Profiles Before Learning',
          2: 'Hebbian and Anti-Hebbian Weight Profiles Before Learning',
          3: 'Hebbian and Homeostatic Weight Profiles Before Learning'}

title_dic_aft= {1:'Hebbian Control Condition Weight Profiles After Learning',
          2: 'Hebbian and Anti-Hebbian Weight Profiles After Learning',
          3: 'Hebbian and Homeostatic Weight Profiles After Learning'}

pathdict= {1:'/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/learning/Hebb',
          2: '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/learning/anti',
          3: '/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/figures/learning/scal'}

def save_fig(fig, path):
    fig.savefig(path, bbox_inches="tight")

def plot_data(ex,in1, in2, title, path):
    counter=1
    for pop in [ex, in1, in2]:
        # df=pd.DataFrame(data=pop)
        col=col_dic.get(counter)
        # output= pop.set_index(0).plot(title='Inhibitory Population 1 av weights by signal group')
        plt.scatter(pop[:,0], pop[:,1], c=col, s=4, label=pop_dic.get(counter))
        plt.ylim(bottom=0, top=2.5)
        plt.xlabel('Signal Group')
        plt.ylabel('Weight')
        counter+=1
    plt.legend()
    # plt.title(title)
    save_fig(plt, path)
    plt.show()



 # Get before plots

alldata=[hebb_hebb_wts, hebb_anti_wts, hebb_scal_wts]
count=1
for data in alldata:
    ex,in1,in2= process_data(data, 1)
    plot_data(ex,in1,in2, title_dic_bef.get(count), str(pathdict.get(count))+'/new_before')
    count+=1

 # Get after plots

alldata=[hebb_hebb_wts, hebb_anti_wts, hebb_scal_wts]
count=1
for data in alldata:
    ex,in1,in2= process_data(data, 6)
    plot_data(ex,in1,in2, title_dic_aft.get(count), str(pathdict.get(count))+'/new_after')
    count+=1
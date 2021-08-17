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
def process_data(dat):
    dat=dat[:, np.r_[0, 1]] # get final state of the weights
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

pop_dic= {1:'Excitatory pop.',
          2: 'Inhibitory pop. 1',
          3: 'Inhibitory pop. 2'}

title_dic= {1:'Hebbian control condition weight profile',
          2: 'Hebbian and anti-Hebbian weight profile',
          3: 'Hebbian and homeostatic scaling weight profile'}

def plot_data(ex,in1, in2, title):
    counter=1
    for pop in [ex, in1, in2]:
        # df=pd.DataFrame(data=pop)
        col=col_dic.get(counter)
        # output= pop.set_index(0).plot(title='Inhibitory Population 1 av weights by signal group')
        plt.scatter(pop[:,0], pop[:,1], c=col, s=4, label=pop_dic.get(counter))
        plt.ylim(bottom=0, top=2.5)
        plt.xlabel('Signal group')
        plt.ylabel('Weight value')
        counter+=1
    plt.legend()
    plt.title(title)
    plt.show()



alldata=[hebb_hebb_wts, hebb_anti_wts, hebb_scal_wts]
count=1
for data in alldata:
    ex,in1,in2= process_data(data)
    plot_data(ex,in1,in2, title_dic.get(count))
    count+=1


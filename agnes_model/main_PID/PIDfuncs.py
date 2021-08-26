import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.parameters import fir_rat_dic

#%% Define column and filter functions

def pid_cols(dat):
    return dat[['postsynaptic_spks', 'ex_spks_stim', 'in1_spks_stim', 'in2_spks_stim']] #get cols for PID analysis

def pid_p1off_cols(dat):
    return dat[['postsynaptic_spks', 'ex_spks_stim', 'in2_spks_stim']] #get cols for PID analysis

def pid_p2off_cols(dat):
    return dat[['postsynaptic_spks', 'ex_spks_stim', 'in1_spks_stim']] #get cols for PID analysis

def pid_inhib_cols(dat):
    return dat[['postsynaptic_spks', 'in1_spks_stim', 'in2_spks_stim']] #get cols for PID analysis

def filter_data(dat, cond, pw, time): # operates on pandas dataframe input!
    output=dat[dat['subcondition']==cond] # select condition k=1,2,3
    output=output[output['time']==time] # select time point wt=0,1,2,5,10,20
    output=output[output['pathway']==pw] # select pathway pw=1,9
    return output

#%% Define necessary PID functions using infotheory library

rnd = lambda x: np.round(x, decimals=4)

def pid_3D(data): # this is used to get lower level synergies
    dims = np.shape(data)[1]
    it = infotheory.InfoTools(dims, 3)
    it.set_equal_interval_binning([10] * dims, np.min(data, 0), np.max(data, 0))
    it.add_data(data)
    # PID-ing
    mi=it.mutual_info([0, 1, 1])
    r = it.redundant_info([0, 1, 2])
    s = it.synergy([0, 1, 2])
    u1 = it.unique_info([0, 1, 2])
    u2 = it.unique_info([0, 2, 1])
    return rnd(mi), rnd(r), rnd(s), rnd(u1), rnd(u2)

def pid_4D(data):
    dims = np.shape(data)[1]
    it = infotheory.InfoTools(dims, 3)
    it.set_equal_interval_binning([10] * dims, np.min(data, 0), np.max(data, 0))
    it.add_data(data)
    # PID-ing
    mi= it.mutual_info([0, 1, 1, 1])
    u1 = it.unique_info([0, 1, 2, 3])
    u2 = it.unique_info([0, 2, 1, 3])
    u3 = it.unique_info([0, 2, 3, 1]) # the unique variable is where the 1 is!!!!
    r = it.redundant_info([0, 1, 2, 3])
    s = it.synergy([0, 1, 2, 3])
    return rnd(mi), rnd(u1), rnd(u2), rnd(u3), rnd(r), rnd(s)

#%% combine functions above to create full PID table

def PID_table(data):
    df = pd.DataFrame(
        columns=['subcondition', 'pathway', 'time', 'total_mi', 'ex_un', 'in1_un', 'in2_un', 'redundancy', 'synergy', 'mi_13','r_13', 'sy_13', 'un_13','un_31','mi_12','r_12','sy_12','un_12','un_21', 'mi_23','r_23','sy_23', 'un_23', 'un_32']) #create empty dataframe
    for k in [1,2,3]: # for all conditions
        for pw in [1, 9]: # loop over pathways
            for t in [0,1,2,5,10,20]: # loop over time points
                dat= pid_cols(filter_data(data, k, pw, t)).to_numpy()
                dat_in1off = pid_p1off_cols(filter_data(data, k, pw, t)).to_numpy() # excluding inhibitory population 1
                dat_in2off = pid_p2off_cols(filter_data(data, k, pw, t)).to_numpy() # excluding inhibitory population 2
                dat_exoff = pid_inhib_cols(filter_data(data, k, pw, t)).to_numpy() # excluding excitatory population
                mi= u1= u2= u3= r= sy= mi_23= r_23= sy_23= un_23= un_32= mi_13= r_13= sy_13= un_13=un_31= mi_12= r_12= sy_12= un_12=un_21= 0
                if k==1:
                    mi, u1, u2, u3, r, sy = pid_4D(dat)
                    mi_23, r_23, sy_23, un_23, un_32 = pid_3D(dat_exoff)
                if k!=3:
                    mi_13, r_13, sy_13, un_13, un_31 = pid_3D(dat_in1off)
                if k != 2:
                    mi_12, r_12, sy_12, un_12, un_21 = pid_3D(dat_in2off)

                df = df.append({'subcondition': k,
                                'pathway': pw,
                                'time': t,
                                'total_mi': mi,
                                'ex_un': u1,
                                'in1_un': u2,
                                'in2_un': u3,
                                'redundancy': r,
                                'synergy': sy,
                                'mi_13': mi_13,
                                'r_13':r_13,
                                'sy_13':sy_13,
                                'un_13': un_13,
                                'un_31': un_31,
                                'mi_12': mi_12,
                                'r_12': r_12,
                                'sy_12': sy_12,
                                'un_12': un_12,
                                'un_21': un_21,
                                'mi_23': mi_23,
                                'r_23': r_23,
                                'sy_23': sy_23,
                                'un_23': un_23,
                                'un_32': un_32}, ignore_index=True)
    df["time"].replace({2: 2.5}, inplace=True)
    return df

#%% combine functions above to create full PID table

def hebb_PID_table(data):
    df = pd.DataFrame(
        columns=['subcondition', 'pathway', 'time', 'total_mi', 'ex_un', 'in1_un', 'in2_un', 'redundancy', 'synergy', 'mi_13','r_13', 'sy_13', 'un_13','mi_12','r_12','sy_12','un_12', 'mi_23','r_23','sy_23', 'un_23']) #create empty dataframe
    k=1 # just for the top condition i.e. hebbian
    for pw in [1, 9]: # loop over pathways
        for t in [0,1,2,5,10,20]: # loop over time points
            dat= pid_cols(filter_data(data, k, pw, t)).to_numpy()
            dat_in1off = pid_p1off_cols(filter_data(data, k, pw, t)).to_numpy() # excluding inhibitory population 1
            dat_in2off = pid_p2off_cols(filter_data(data, k, pw, t)).to_numpy() # excluding inhibitory population 2
            dat_exoff = pid_inhib_cols(filter_data(data, k, pw, t)).to_numpy() # excluding excitatory population
            mi= u1= u2= u3= r= sy= mi_23= r_23= sy_23= un_23= mi_13= r_13= sy_13= un_13= mi_12= r_12= sy_12= un_12= 0
            if k==1:
                mi, u1, u2, u3, r, sy = pid_4D(dat)
                mi_23, r_23, sy_23, un_23, un_32 = pid_3D(dat_exoff)
            if k!=3:
                mi_13, r_13, sy_13, un_13, un_31 = pid_3D(dat_in1off)
            if k != 2:
                mi_12, r_12, sy_12, un_12, un_21 = pid_3D(dat_in2off)

            df = df.append({'subcondition': k,
                            'pathway': pw,
                            'time': t,
                            'total_mi': mi,
                            'ex_un': u1,
                            'in1_un': u2,
                            'in2_un': u3,
                            'redundancy': r,
                            'synergy': sy,
                            'mi_13': mi_13,
                            'r_13':r_13,
                            'sy_13':sy_13,
                            'un_13': un_13,
                            'mi_12': mi_12,
                            'r_12': r_12,
                            'sy_12': sy_12,
                            'un_12': un_12,
                            'mi_23': mi_23,
                            'r_23': r_23,
                            'sy_23': sy_23,
                            'un_23': un_23}, ignore_index=True)
    df["time"].replace({2: 2.5}, inplace=True)
    return df




import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory

#%% filter functions for data and PID analysis

def filter_data(dat, cond, pw, time):
    output=dat[dat[:,1]==cond,:] # select condition k=1,2,3
    output=output[output[:,2]==time,:] # select time point wt=0,1,2,5,10,20
    output=output[output[:,3]==pw,:] # select pathway pw=1,9
    return output

def pid_cols(dat):
    return dat[:, [5, 9, 10, 11]] #get cols for PID analysis

#%% Define necessary PID functions using infotheory library
rnd = lambda x: np.round(x, decimals=4)

def get_pid_3D(data):
    dims = np.shape(data)[1]
    it = infotheory.InfoTools(dims, 3)
    it.set_equal_interval_binning([10] * dims, np.min(data, 0), np.max(data, 0))
    it.add_data(data)
    # PID-ing
    u1 = it.unique_info([0, 1, 2])
    u2 = it.unique_info([0, 2, 1])
    r = it.redundant_info([0, 1, 2])
    s = it.synergy([0, 1, 2])
    return rnd(u1), rnd(u2), rnd(r), rnd(s)

def get_pid_4D(data):
    dims = np.shape(data)[1]
    it = infotheory.InfoTools(dims, 3)
    it.set_equal_interval_binning([10] * dims, np.min(data, 0), np.max(data, 0))
    it.add_data(data)
    # PID-ing
    mi= it.mutual_info([0, 1, 2, 3])
    u1 = it.unique_info([0, 1, 2, 3])
    u2 = it.unique_info([0, 2, 1, 3])
    u3 = it.unique_info([0, 2, 3, 1])
    r = it.redundant_info([0, 1, 2, 3])
    s = it.synergy([0, 1, 2, 3])
    return rnd(mi), rnd(u1), rnd(u2), rnd(u3), rnd(r), rnd(s)

def plot_pid(subplot_ind, data, u1, u2, r, sy, title, u3=None):
    # plt.subplot(subplot_ind)
    plt.scatter(
        np.linspace(0, 1, len(data[:, 0])),
        data[:, 0],
        label="T - Target",
        s=2,
        alpha=0.7,
    )
    plt.scatter(
        np.linspace(0, 1, len(data[:, 1])),
        data[:, 1],
        label="X - Source 1",
        s=2,
        alpha=0.7,
    )
    plt.scatter(
        np.linspace(0, 1, len(data[:, 2])),
        data[:, 2],
        label="Y - Source 2",
        s=2,
        alpha=0.7,
    )
    if np.shape(data)[1] == 4:
        plt.scatter(
            np.linspace(0, 1, len(data[:, 3])),
            data[:, 3],
            label="Z - Source 3",
            s=2,
            alpha=0.7,
        )
        title = title + "\n[u_x,u_y, u_z]={}\n[r,sy]={}".format([u1, u2, u3], [r, sy])
    else:
        title = title + "\n[u_x,u_y]={}\n[r,sy]={}".format([u1, u2], [r, sy])

    plt.title(title, fontsize=10)
    plt.legend(bbox_to_anchor=[1.1, 1.1])

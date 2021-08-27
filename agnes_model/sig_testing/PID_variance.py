# THIS FILE CREATES PID PLOTS WITH ERROR BARS FOR STANDARD DEVIATION!

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *
from agnes_model.main_PID.PIDfuncs import *

#%% Import list of data from pickle
file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/all_variance.pkl"

open_file = open(file_name, "rb")
runs = pickle.load(open_file)
open_file.close()

#%% Import list of data from pickle

for listo in runs:
    for df in listo:
        df=df.drop(columns='run')

#%%
hebb=runs[0]+runs[1]
anti=runs[2]+runs[3]
scal=runs[4]+runs[5]

hebb_PIDs=[hebb_PID_table(hebb[i]) for i in range(10)]
anti_PIDs= [PID_table(anti[i]) for i in range(10)]
scal_PIDs= [PID_table(scal[i]) for i in range(10)]

#%% these are the mean and std tables
n=10 # this is for if standard error is calculated

hebb_final = pd.concat(hebb_PIDs).groupby(['subcondition','pathway', 'time']).agg(['mean', 'std']).reset_index()
anti_final = pd.concat(anti_PIDs).groupby(['subcondition','pathway', 'time']).agg(['mean', 'std']).reset_index()
scal_final = pd.concat(scal_PIDs).groupby(['subcondition','pathway', 'time']).agg(['mean', 'std']).reset_index()

#%% these are the mean vals- the reported result values!

hebb_result = pd.concat(hebb_PIDs).groupby(['subcondition','pathway', 'time']).mean().reset_index()
anti_result = pd.concat(anti_PIDs).groupby(['subcondition','pathway', 'time']).mean().reset_index()
scal_result = pd.concat(scal_PIDs).groupby(['subcondition','pathway', 'time']).mean().reset_index()

results=[hebb_result, anti_result, scal_result]
#%% export results
file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/results.pkl"

open_file = open(file_name, "wb")
pickle.dump(results, open_file)
open_file.close()

#%% All dictionaries for names of columns/variables

col_dic={'time_':'Time',
         'total_mi_mean': "$I(X_{1}, X_{2}, X_{3}; T)$",
         'redundancy_mean': '$I_{\partial}^{\{1\} \{2\} \{3\}}$',
         'ex_un_mean': '$I_{\partial}^{\{1\}}$',
         'synergy_mean': '$I_{\partial}^{\{1 2 3\}}$',
         'sy_12_mean': '$I_{\partial}^{\{1 2\}}*$',
         'sy_13_mean': '$I_{\partial}^{\{1 3\}}*$'}

pref_col_dic_p1off={'time_':'Time',
                'mi_13_mean':'$I(X_{1}, X_{3}; T)$',
                'r_13_mean':'$I_{\partial}^{\{1\} \{3\}}$',
                'un_13_mean': '$I_{\partial}^{\{1\}}$',
                'sy_13_mean': '$I_{\partial}^{\{1 3\}}$'}

nonpref_col_dic_p1off={'time_':'Time',
                       'mi_13_mean':'$I(Y_{1}, Y_{3}; T)$',
                       'r_13_mean':'$I_{\partial}^{\{1\} \{3\}}$',
                       'un_13_mean': '$I_{\partial}^{\{1\}}$',
                       'sy_13_mean': '$I_{\partial}^{\{1 3\}}$'}

pref_col_dic_p2off={'time_':'Time',
                    'mi_12_mean': '$I(X_{1}, X_{2}; T)$',
                    'r_12_mean': '$I_{\partial}^{\{1\} \{2\}}$',
                    'un_12_mean': '$I_{\partial}^{\{1\}}$',
                    'sy_12_mean': '$I_{\partial}^{\{1 2\}}$'}

nonpref_col_dic_p2off={'time_':'Time',
                       'mi_12_mean': '$I(Y_{1}, Y_{2}; T)$',
                       'r_12_mean': '$I_{\partial}^{\{1\} \{2\}}$',
                       'un_12_mean': '$I_{\partial}^{\{1\}}$',
                       'sy_12_mean': '$I_{\partial}^{\{1 2\}}$'}

main_col_dic={1:{1:col_dic, 9: col_dic}, # both populations on
              2:{1: nonpref_col_dic_p1off, 9: pref_col_dic_p1off}, # pop 1 off
              3:{1: nonpref_col_dic_p2off, 9: pref_col_dic_p2off}} # pop 2 off

#%% Plot PID function with error bars


def plot_err_bar(data, big_col_dict, cond, pw, fold_path):
    fullpath=str(fold_path)+'/ERR_cond_'+str(cond)+'_pw'+str(pw)
    col_dict=big_col_dict.get(cond).get(pw)
    fig,ax = plt.subplots()
    df=data[data['pathway']==pw]
    df = df[df['subcondition'] == cond]
    df.columns = ['_'.join(col).strip() for col in df.columns.values] # flatten the index
    cols=list(col_dict.keys())
    colours= [u'#1f77b4', u'#d62728', u'#2ca02c', u'#ff7f0e', u'#e377c2', u'#7f7f7f', u'#bcbd22', u'#17becf']
    cols.remove('time_')
    for count, i in enumerate(cols):
        std_str=i.replace('mean', 'std')
        ax.errorbar(x = df["time_"],
                    y=df[i],
                    yerr=df[std_str],
                    label=col_dict.get(i),
                    color= colours[count],
                    ecolor='black',
                    capsize=2)
        # ax.scatter(x = df["time_"], y=df[i], marker=markers[count], zorder=1)
    ax.legend()
    ax.set_ylabel('Bits')
    ax.set_xlabel('Time (mins)')
    plt.savefig(fullpath, bbox_inches="tight")
    plt.show()

hebb_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/new_figures/PIDs/Hebb'
anti_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/new_figures/PIDs/anti'
scal_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/new_figures/PIDs/scal'

#%% make hebbian plots
plot_err_bar(hebb_final, main_col_dic, 1, 9, hebb_path)
plot_err_bar(hebb_final, main_col_dic, 1, 1, hebb_path)


#%% make anti-hebbian plots
for cond in [1,2,3]:
    for pw in [1,9]:
        plot_err_bar(anti_final, main_col_dic, cond, pw, anti_path)

#%% make homeostatic scaling plots
for cond in [1,2,3]:
    for pw in [1,9]:
        plot_err_bar(scal_final, main_col_dic, cond, pw, scal_path)


#%% export results
file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/all_variance.pkl"

open_file = open(file_name, "rb")
runs = pickle.load(open_file)
open_file.close()


PID_runs=[full_PID_dataframe(get_firing_rates(df)) for df in runs]

#%% Concat and calculate mean and std/var of atoms

df_PID = pd.concat(PID_runs).groupby(['subcondition','pathway', 'time']).agg(['mean', 'var'])

# Here we can see that the variance is very small across all the dataframes, the standard deviation is larger.
# Results seem to be fairly consistent


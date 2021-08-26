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

#%%
# n=10
#
# mean_hebb = pd.concat(hebb_PIDs).groupby(['subcondition','pathway', 'time']).mean().reset_index()
# std_hebb = pd.concat(hebb_PIDs).groupby(['subcondition','pathway', 'time']).std().reset_index()
#
# mean_anti = pd.concat(anti_PIDs).groupby(['subcondition','pathway', 'time']).mean().reset_index()
# std_anti = pd.concat(anti_PIDs).groupby(['subcondition','pathway', 'time']).std().reset_index()
#
# mean_scal = pd.concat(scal_PIDs).groupby(['subcondition','pathway', 'time']).mean().reset_index()
# std_scal = pd.concat(scal_PIDs).groupby(['subcondition','pathway', 'time']).std().reset_index()


#%%
n=10 # this is for if standard error is calculated

hebb_final = pd.concat(hebb_PIDs).groupby(['subcondition','pathway', 'time']).agg(['mean', 'std']).reset_index()
anti_final = pd.concat(anti_PIDs).groupby(['subcondition','pathway', 'time']).agg(['mean', 'std']).reset_index()
scal_final = pd.concat(scal_PIDs).groupby(['subcondition','pathway', 'time']).agg(['mean', 'std']).reset_index()

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

#%% All dictionaries for names of columns/variables

def plot_err_bar(data, big_col_dict, pw, cond):
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
    plt.show()


plot_err_bar(scal_final, main_col_dic, 1, 3)

#%%

col_dic={'time_':'Time',
         'total_mi_mean': "$I(X_{1}, X_{2}, X_{3}; T)$",
         'redundancy_mean': '$I_{\partial}^{\{1\} \{2\} \{3\}}$',
         'ex_un_mean': '$I_{\partial}^{\{1\}}$',
         'synergy_mean': '$I_{\partial}^{\{1 2 3\}}$',
         'sy_12_mean': '$I_{\partial}^{\{1 2\}}*$',
         'sy_13_mean': '$I_{\partial}^{\{1 3\}}*$'}

fig,ax = plt.subplots()
df=hebb_final[hebb_final['pathway']==9]
df.columns = ['_'.join(col).strip() for col in df.columns.values] # flatten the index
cols=list(col_dic.keys())
cols.remove('time_')
for i in cols:
    std_str=i.replace('mean', 'std')
    ax.errorbar(x = df["time_"],
                y=df[i],
                yerr=df[std_str],label=col_dic.get(i))
# ax.axhline(y=0 , color='r', linestyle='--')
ax.legend()
plt.show()















#%%

# #%% plot results
#
# plastic_dic={1: ' (Hebbian)', 2: ' (Anti-Hebbian)', 3: ' (Homeostatic Scaling)'}
# title_dic_4d={1: 'PID Atoms for non-Preferred Pathway',
#            9:'PID Atoms for Preferred Pathway'}
# pref_col_dic={'time':'Time', 'total_mi': "$I(X_{1}, X_{2}, X_{3}; T)$", 'redundancy': '$I_{\partial}^{\{1\} \{2\} \{3\}}$', 'ex_un': '$I_{\partial}^{\{1\}}$', 'synergy': '$I_{\partial}^{\{1 2 3\}}$', 'sy_12': '$I_{\partial}^{\{1 2\}}*$', 'sy_13': '$I_{\partial}^{\{1 3\}}*$'}
# nonpref_col_dic={'time':'Time', 'total_mi': "$I(Y_{1}, Y_{2}, Y_{3}; T)$", 'redundancy': '$I_{\partial}^{\{1\} \{2\} \{3\}}$', 'ex_un': '$I_{\partial}^{\{1\}}$', 'synergy': '$I_{\partial}^{\{1 2 3\}}$', 'sy_12': '$I_{\partial}^{\{1 2\}}*$', 'sy_13': '$I_{\partial}^{\{1 3\}}*$'}
#
#
#
# pref_dics={1: nonpref_col_dic, 9: pref_col_dic}
#
# # mult=100 # this is to test plotting function
# # std_hebb*=mult
# # std_hebb[['subcondition', 'pathway', 'time']]/=mult
#
# def plot_PID(tb,err_tb, pw, condition):
#     # path=str(path_dic.get(condition))+'/new_PID_pw'+str(pw)
#     title=str(title_dic_4d.get(pw)) +str(plastic_dic.get(condition))
#     # print(filter_condition(tb, 1, pw).columns)
#     plot_table = filter_condition(tb, 1, pw).rename(columns=pref_dics.get(pw))
#     cols=list(pref_dics.get(pw).values())
#     cols.remove('Time')
#     lines = plot_table.plot.line(style=['.-','-x','-o','-s','-*','-d'], x='Time', y=cols ,color = ['royalblue', 'red', 'forestgreen','purple', 'orange', 'yellow'])
#     lines.set_ylabel('Bits')
#     lines.set_xlabel('Time (mins)')
#     # lines.plot(yerr=err_tb, legend=False)
#     lines.errorbar(x=plot_table['Time'], y=plot_table[cols], yerr=err_tb)
#     # lines.figure.savefig(path, bbox_inches="tight")
#     lines.figure.show()
#
# plot_PID(mean_hebb, std_hebb, 9, 1)


#%% export results
# file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/all_variance.pkl"
#
# open_file = open(file_name, "rb")
# runs = pickle.load(open_file)
# open_file.close()

#
# PID_runs=[full_PID_dataframe(get_firing_rates(df)) for df in runs]
#
# #%% Concat and calculate mean and std/var of atoms
#
# df_PID = pd.concat(PID_runs).groupby(['subcondition','pathway', 'time']).agg(['mean', 'var'])
#
# # Here we can see that the variance is very small across all the dataframes, the standard deviation is larger.
# # Results seem to be fairly consistent
#

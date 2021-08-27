# THIS FILE COMPARES THE OUR PID VALUES TO SURROGATE ONES AND DETERMINES STATISTICAL SIGNIFICANCE I.E. TESTS NULL HYPOTHESIS
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import infotheory
from agnes_model.step_input.functions import *
from agnes_model.main_PID.PIDfuncs import *

#%% Import list of data from pickle
file_name = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/surrogate/75_surr_PIDs.pkl"

open_file = open(file_name, "rb")
surrs = pickle.load(open_file)
open_file.close()

#%% Import list of data from pickle
results_file = "/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/processed_data/results.pkl"

open_file = open(results_file, "rb")
results = pickle.load(open_file)
open_file.close()

#%% Import list of data from pickle

hebb_PIDs=surrs[0]
anti_PIDs= surrs[1]
scal_PIDs= surrs[2]

#%% Gaussianity check: can check individual values
val_list=[]
for tab in hebb_PIDs:
    val_list.append(tab.loc[8, 'synergy'])
plt.hist(val_list, bins=8)
plt.show()

#%% Get means and standard deviations
n=75

mean_hebb = pd.concat(hebb_PIDs).groupby(['subcondition','pathway', 'time']).mean().reset_index()
std_hebb = pd.concat(hebb_PIDs).groupby(['subcondition','pathway', 'time']).std().reset_index()

mean_anti = pd.concat(anti_PIDs).groupby(['subcondition','pathway', 'time']).mean().reset_index()
std_anti = pd.concat(anti_PIDs).groupby(['subcondition','pathway', 'time']).std().reset_index()

mean_scal = pd.concat(scal_PIDs).groupby(['subcondition','pathway', 'time']).mean().reset_index()
std_scal = pd.concat(scal_PIDs).groupby(['subcondition','pathway', 'time']).std().reset_index()


#%% Get comparison dataframes
sd_mult=4 # how many standard deviations from the mean

hebb_comp=mean_hebb+sd_mult*std_hebb.values
anti_comp=mean_anti+sd_mult*std_anti.values
scal_comp=mean_scal+sd_mult*std_scal.values



#%% get difference between dataframes

actual_hebb=results[0]
actual_anti=results[1].drop(columns=['un_31', 'un_21', 'un_32'])
actual_scal=results[2].drop(columns=['un_31', 'un_21', 'un_32'])

hebb_sig=actual_hebb-hebb_comp.values
anti_sig=actual_anti-anti_comp.values
scal_sig=actual_scal-scal_comp.values

hebb_sig[['subcondition', 'pathway', 'time']]=actual_hebb[['subcondition', 'pathway', 'time']]
anti_sig[['subcondition', 'pathway', 'time']]=actual_anti[['subcondition', 'pathway', 'time']]
scal_sig[['subcondition', 'pathway', 'time']]=actual_scal[['subcondition', 'pathway', 'time']]

#%% create binary truth tables for indicating significance
hebb_ind=hebb_sig.copy()
anti_ind=anti_sig.copy()
scal_ind=scal_sig.copy()

hebb_ind[hebb_ind>0.001]=1
hebb_ind[hebb_ind<=0.001]=0
anti_ind[anti_ind>0.001]=1
anti_ind[anti_ind<=0.001]=0
scal_ind[scal_ind>0.001]=1
scal_ind[scal_ind<=0.001]=0

hebb_ind[['subcondition', 'pathway', 'time']]=actual_hebb[['subcondition', 'pathway', 'time']]
anti_ind[['subcondition', 'pathway', 'time']]=actual_anti[['subcondition', 'pathway', 'time']]
scal_ind[['subcondition', 'pathway', 'time']]=actual_scal[['subcondition', 'pathway', 'time']]

#%% create binary truth tables for indicating significance

hebb_full = pd.merge(actual_hebb,
                     hebb_ind,
                     how='left',
                     left_on=['subcondition', 'pathway', 'time'],
                     right_on = ['subcondition', 'pathway', 'time'],
                     suffixes=('_mean', '_ind'))

anti_full = pd.merge(actual_anti,
                     anti_ind,
                     how='left',
                     left_on=['subcondition', 'pathway', 'time'],
                     right_on = ['subcondition', 'pathway', 'time'],
                     suffixes=('_mean', '_ind'))

scal_full = pd.merge(actual_scal,
                     scal_ind,
                     how='left',
                     left_on=['subcondition', 'pathway', 'time'],
                     right_on = ['subcondition', 'pathway', 'time'],
                     suffixes=('_mean', '_ind'))
#%% All dictionaries for names of columns/variables

col_dic={'time':'Time',
         # 'total_mi_mean': "$I(X_{1}, X_{2}, X_{3}; T)$",
         'redundancy_mean': '$I_{\partial}^{\{1\} \{2\} \{3\}}$',
         'ex_un_mean': '$I_{\partial}^{\{1\}}$',
         'synergy_mean': '$I_{\partial}^{\{1 2 3\}}$',
         'sy_12_mean': '$I_{\partial}^{\{1 2\}}*$',
         'sy_13_mean': '$I_{\partial}^{\{1 3\}}*$'}

pref_col_dic_p1off={'time':'Time',
                # 'mi_13_mean':'$I(X_{1}, X_{3}; T)$',
                'r_13_mean':'$I_{\partial}^{\{1\} \{3\}}$',
                'un_13_mean': '$I_{\partial}^{\{1\}}$',
                'sy_13_mean': '$I_{\partial}^{\{1 3\}}$'}

nonpref_col_dic_p1off={'time':'Time',
                       # 'mi_13_mean':'$I(Y_{1}, Y_{3}; T)$',
                       'r_13_mean':'$I_{\partial}^{\{1\} \{3\}}$',
                       'un_13_mean': '$I_{\partial}^{\{1\}}$',
                       'sy_13_mean': '$I_{\partial}^{\{1 3\}}$'}

pref_col_dic_p2off={'time':'Time',
                    # 'mi_12_mean': '$I(X_{1}, X_{2}; T)$',
                    'r_12_mean': '$I_{\partial}^{\{1\} \{2\}}$',
                    'un_12_mean': '$I_{\partial}^{\{1\}}$',
                    'sy_12_mean': '$I_{\partial}^{\{1 2\}}$'}

nonpref_col_dic_p2off={'time':'Time',
                       # 'mi_12_mean': '$I(Y_{1}, Y_{2}; T)$',
                       'r_12_mean': '$I_{\partial}^{\{1\} \{2\}}$',
                       'un_12_mean': '$I_{\partial}^{\{1\}}$',
                       'sy_12_mean': '$I_{\partial}^{\{1 2\}}$'}

main_col_dic={1:{1:col_dic, 9: col_dic}, # both populations on
              2:{1: nonpref_col_dic_p1off, 9: pref_col_dic_p1off}, # pop 1 off
              3:{1: nonpref_col_dic_p2off, 9: pref_col_dic_p2off}} # pop 2 off
#%% plot the results

def plot_sig(data, big_col_dict, cond, pw,fold_path): # this is the plot function used for normalised plots
    fullpath=str(fold_path)+'/NORM_cond_'+str(cond)+'_pw'+str(pw)
    col_dict=big_col_dict.get(cond).get(pw)
    fig,ax = plt.subplots()
    df=data[data['pathway']==pw]
    df = df[df['subcondition'] == cond]
    cols=list(col_dict.keys())
    colours= [u'#d62728', u'#2ca02c', u'#ff7f0e', u'#e377c2', u'#7f7f7f', u'#bcbd22', u'#17becf']
    cols.remove('time')
    for count, i in enumerate(cols):
        ind_str=i.replace('_mean', '_ind')
        df_sig=df[df[ind_str]==1]
        df_nonsig = df[df[ind_str] == 0]
        ax.errorbar(x = df["time"],
                    y=df[i],
                    label=col_dict.get(i),
                    color= colours[count],
                    zorder=1)
        if count==0: # include label for first plot
            ax.scatter(x = df_sig["time"], y=df_sig[i], marker='o', zorder=2, label='Significant', facecolors='none', edgecolors='grey')
            ax.scatter(x=df_nonsig["time"], y=df_nonsig[i], marker='x', zorder=2, label='Non-significant', color='grey')
        else:
            ax.scatter(x=df_sig["time"], y=df_sig[i], marker='o', zorder=2, facecolors='none',
                       edgecolors='grey')
            ax.scatter(x=df_nonsig["time"], y=df_nonsig[i], marker='x', zorder=2, color='grey')
    ax.legend()
    ax.set_ylabel('Normalised information')
    ax.set_xlabel('Time (mins)')
    plt.ylim(top= 1)
    plt.savefig(fullpath, bbox_inches="tight")
    plt.show()

# plot_sig(scal_full, main_col_dic, 9, 1)

#%% normalise data

def normalise_PID(data, condition): # this only works with the filter on the condition!
    df = data[data['subcondition'] == condition]
    both_on=['ex_un_mean', 'in1_un_mean', 'in2_un_mean', 'redundancy_mean', 'synergy_mean', 'r_13_mean', 'sy_13_mean', 'un_13_mean', 'r_12_mean', 'sy_12_mean', 'un_12_mean']
    p1_off=['r_13_mean', 'sy_13_mean', 'un_13_mean']
    p2_off=['r_12_mean', 'sy_12_mean', 'un_12_mean']
    mutual_infos=['total_mi_mean', 'mi_13_mean', 'mi_12_mean']
    columns=[both_on, p1_off, p2_off]
    output=df.copy()
    output[columns[condition - 1]] = output[columns[condition - 1]].div(output[mutual_infos[condition - 1]], axis=0)
    return output

def plot_condition(data, condition, pathway, fold): # final plot condition
    plot_sig(normalise_PID(data, condition), main_col_dic, condition, pathway,  fold)

hebb_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/new_figures/PIDs/Hebb'
anti_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/new_figures/PIDs/anti'
scal_path='/Users/JoeCussen/Documents/CCNSheff/Project/Modelling/infotheoryproject/agnes_model/new_figures/PIDs/scal'


# plot_condition(hebb_full, 1, 9, hebb_path)

#%% make hebbian plots
plot_condition(hebb_full, 1, 9, hebb_path)
plot_condition(hebb_full, 1, 1, hebb_path)

#%% make anti-hebbian plots
for cond in [1,2,3]:
    for pw in [1,9]:
        plot_condition(anti_full, cond, pw, anti_path)

#%% make homeostatic scaling plots
for cond in [1,2,3]:
    for pw in [1,9]:
        plot_condition(scal_full, cond, pw, scal_path)

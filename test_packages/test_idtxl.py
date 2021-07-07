import numpy as np
from idtxl.multivariate_pid import MultivariatePID
from idtxl.data import Data

#%%
# a) Generate test data
n = 100
alph = 2
x = np.random.randint(0, alph, n)
y = np.random.randint(0, alph, n)
z = np.logical_xor(x, y).astype(int)
data = Data(np.vstack((x, y, z)), 'ps', normalise=False)

# b) Initialise analysis object and define settings for SxPID estimators
pid = MultivariatePID()
settings_SxPID = {'pid_estimator': 'SxPID', 'lags_pid': [0, 0]}

# c) Run Goettingen estimator
results_SxPID = pid.analyse_single_target(
    settings=settings_SxPID, data=data, target=2, sources=[0, 1])


# e) Print results to console
print('\nLogical XOR')
print('Estimator            SxPID\t\tExpected\n')
print('Uni s1               {0:.4f}\t\t{1:.4f}'.format(
    results_SxPID.get_single_target(2)['avg'][((1,),)][2],
    .5896))
print('Uni s2               {0:.4f}\t\t{1:.4f}'.format(
    results_SxPID.get_single_target(2)['avg'][((2,),)][2],
    0.5896))
print('Shared s1_s2         {0:.4f}\t\t{1:.4f}'.format(
    results_SxPID.get_single_target(2)['avg'][((1,),(2,),)][2],
    -0.5896))
print('Synergy s1_s2        {0:.4f}\t\t{1:.4f}'.format(
    results_SxPID.get_single_target(2)['avg'][((1,2,),)][2],
    0.415))

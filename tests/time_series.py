#%% md

# Time Series Analysis

# One important area of application for information theory is time series analysis. Here, we will demonstrate how to compute the *modes of information flow* --- intrinsic, shared, and synergistic --- between the two dimensions of the [tinkerbell attractor](https://en.wikipedia.org/wiki/Tinkerbell_map).

#%%

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

import dit
from dit.inference import binned, dist_from_timeseries
from dit.multivariate import total_correlation as I, intrinsic_total_correlation as IMI

dit.ditParams['repr.print'] = True

#%% md

# Here we define a few constants for this notebook:

#%%

TRANSIENTS = 1000
ITERATIONS = 1000000
BINS = 3
HISTORY_LENGTH = 2

#%% md

## Generating the Time Series

# We write a generator for our two time series:

#%%

def tinkerbell(x=None, y=None, a=0.9, b=-0.6013, c=2.0, d=0.5):
    if x is None:
        x = np.random.random() - 1
    if y is None:
        y = np.random.random() - 1
    while True:
        x, y = x**2 - y**2 + a*x + b*y, 2*x*y + c*x + d*y
        yield x, y

#%% md

# And then we generate the time series:

#%%

tb = tinkerbell()

# throw away transients
[next(tb) for _ in range(TRANSIENTS)]

time_series = np.asarray([next(tb) for _ in range(ITERATIONS)])

#%% md

# And we plot the attractor because it's pretty:

#%%

plt.figure(figsize=(8, 6))
plt.scatter(time_series[:,0], time_series[:,1], alpha=0.1, s=0.01)
plt.show()

#%%

# Plot distribution of time series x values:
plt.figure(3)
pd.Series(time_series[:,0]).plot.hist(bins=40, rwidth=0.9,
                   color='blue', alpha=0.4)
pd.Series(time_series[:,1]).plot.hist(bins=40, rwidth=0.9,
                   color='red', alpha=0.4)
plt.title('Distribution of the tinkerbell function x & y coordinates')
plt.xlabel('Value')
plt.ylabel('Counts')
plt.legend('x', 'y')
plt.show()

# Note that these distributions are not normal so binning is appropriate for this kind of data!


#%% md



## Discretizing the Time Series

#%%

binary_time_series = binned(time_series, bins=BINS)

#%%

print(binary_time_series[:10])

#%% Compare the time series and visualise the points by their discretization

df = pd.DataFrame(np.concatenate((time_series, binary_time_series), axis=1))
df.columns= ['x', 'y', 'x_bin', 'y_bin']

#%%
# look at the x bin max entropy cutoffs
groups = df.groupby("x_bin")
plt.figure(0)
for name, group in groups:
    plt.plot(group["x"], group["y"], marker="o", linestyle="", label=name)
plt.legend()
plt.show()

#%%
# look at the x max entropy cutoffs
groups = df.groupby("y_bin")
plt.figure(1)
for name, group in groups:
    plt.plot(group["x"], group["y"], marker="o", linestyle="", label=name)
plt.legend()
plt.show()




#%% md

## Constructing a Distribution from the Time Series

#%%

time_series_distribution = dist_from_timeseries(binary_time_series, history_length=HISTORY_LENGTH)

#%%

time_series_distribution

#%% md

# Finally, we assign helpful variable names to the indicies of the distribution:

#%%

x_past = [0]
y_past = [1]
x_pres = [2]
y_pres = [3]

#%% md

## Measuring the Modes of Information Flow

#%%

intrinsic_x_to_y = IMI(time_series_distribution, [x_past, y_pres], y_past)
time_delayed_mutual_information_x_to_y = I(time_series_distribution, [x_past, y_pres])
transfer_entropy_x_to_y = I(time_series_distribution, [x_past, y_pres], y_past)

shared_x_to_y = time_delayed_mutual_information_x_to_y - intrinsic_x_to_y
synergistic_x_to_y = transfer_entropy_x_to_y - intrinsic_x_to_y

#%%

print(f"Flows from x to y:\n\tIntrinsic: {intrinsic_x_to_y}\n\tShared: {shared_x_to_y}\n\tSynergistic: {synergistic_x_to_y}")

#%%

intrinsic_y_to_x = IMI(time_series_distribution, [y_past, x_pres], x_past)
time_delayed_mutual_informtaion_y_to_x = I(time_series_distribution, [y_past, x_pres])
transfer_entropy_y_to_x = I(time_series_distribution, [y_past, x_pres], x_past)

shared_y_to_x = time_delayed_mutual_informtaion_y_to_x - intrinsic_y_to_x
synergistic_y_to_x = transfer_entropy_y_to_x - intrinsic_y_to_x

#%%

print(f"Flows from y to x:\n\tIntrinsic: {intrinsic_y_to_x}\n\tShared: {shared_y_to_x}\n\tSynergistic: {synergistic_y_to_x}")

#%%



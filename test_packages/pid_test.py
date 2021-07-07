#%% md

# Partial Information Decomposition

# The partial information decomposition is a method of decomposing the mutual information between a set of sources, $X_0, X_1, \ldots$ and a target $Y$: $I\left[X_0, X_1, \ldots : Y\right]$. In the bivariate sources case, the decomposition takes a particularly intuitive form: There is redundant information, unique information from $X_0$, unique information from $X_1$, and synergistic information.

# There are many proposals for how to quantify this decomposition. Here, we explore the behavior of many of these proposals on a wide variety of distribution. This survey helps clarify commonalities and differences is the variety of proposed approaches.

#%%

import dit
from dit.pid.helpers import compare_measures
from dit.pid.distributions import bivariates, trivariates
dit.ditParams['print.exact'] = dit.ditParams['repr.print'] = True
dit.ditParams['text.font'] = 'linechar'

#%% md

# Survey

## Bivariate

# If `colorama` is installed, measure names that are green indicate that some partial information values are negative, measure names that are blue indicate that the lattice could not be completely computed, and measure names that are red indicate that the measure resulted in an inconsistancy in the lattice.

#%%

for name, dist in bivariates.items():
    print(name)
    print(dist)
    #compare_measures(dist, name=name)

#%% md

## Trivariate

# In the example distributions "xor cat" and "dbl xor" below, it is widely believed that the negativity seen in many of the measures is a result not of a failure of the measure, but rather a sign that the redundancy lattice is not complete.

#%%

for name, dist in trivariates.items():
    print(name)
    print(dist)
    # compare_measures(dist, name=name)

#%%
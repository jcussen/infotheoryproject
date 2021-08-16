

n_pw = 16 # number of pathways
ne_pw = 200 # number of excitatory neurons per pathway
ni_pw1 = 25 # number of inhibitory neurons per pathway in inhib pop 1
ni_pw2 = 25 # number of inhibitory neurons type 2 per pathway
ne = n_pw * ne_pw # total number of pre - synaptic excitatory neurons
ni1 = n_pw * ni_pw1 # total number of pre - synaptic inhib pop1 neurons
ni2 = n_pw * ni_pw2 # total number of pre - synaptic inhib pop2 neurons
tot_n = ne + ni1 + ni2 # total number of presynaptic neurons
pref_pw = 9 # preferred input signal number
window= 0.05 # seconds i.e. 50 ms - the size of the phasic response window

post_mult=1/window # postsynaptic firing rate multiplier
ex_mult_total=post_mult/ne # excitatory pop total multiplier
in1_mult_total=post_mult/ni1 # inhib pop 1 total multiplier
in2_mult_total=post_mult/ni2 # inhib pop 2 pop total multiplier

ex_mult_path=post_mult/ne_pw # excitatory pop pathway multiplier
in1_mult_path=post_mult/ni_pw1 # inhib pop 1 pathway multiplier
in2_mult_path=post_mult/ni_pw2 # inhib pop 2 pop pathway multiplier

# Firing rate multiplier dictionary

fir_rat_dic= {
    'postsynaptic_spks': post_mult,
    'ex_spks_total': ex_mult_total,
    'in1_spks_total': in1_mult_total,
    'in2_spks_total': in2_mult_total,
    'ex_spks_stim': ex_mult_path,
    'in1_spks_stim': in1_mult_path,
    'in2_spks_stim': in2_mult_path
}
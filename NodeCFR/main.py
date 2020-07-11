import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import Utilities as U
import Exploiter as E
from NodeCFR.CounterfactualRegretMinimizationBase import *
from NodeCFR.ChanceSamplingCFR import *
from NodeCFR.VanillaCFR import *

def nodecfr(nodes, infosets, abs_infosets, game, method = 'public_chance', T = 1000, verbose = False):
# Enriching the nodes and abstract infosets dataframe
    n_abstract = len(abs_infosets.index)
    U.update_natureprob(nodes)
    U.maptoclust(infosets, abs_infosets)
    U.abstractnodes(nodes, abs_infosets, infosets)
    U.abstractsons(nodes, abs_infosets, infosets)
    U.abstractdads(abs_infosets)
    U.abs_depth(abs_infosets)
    U.nodetoclust(nodes, infosets, abs_infosets)
    #abs_infosets = U.chance_to_infoset(nodes, infosets, abs_infosets)

    if method == 'public_chance':
        chance_sampling_cfr = ChanceSamplingCFR(nodes)
        chance_sampling_cfr.run(iterations = T)
        U.get_back(infosets, abs_infosets, chance_sampling_cfr.nash_equilibrium)

    elif method == 'vanilla':
        vanilla_cfr = VanillaCFR(nodes)
        vanilla_cfr.run(iterations = T)
        U.get_back(infosets, abs_infosets, vanilla_cfr.nash_equilibrium)

    probos = [[] for _ in range(len(infosets.index))]
    for i,row in abs_infosets.head(n_abstract).iterrows():
        for m in row.Map:
            probos[m].append(row.Actions_Prob)
    infosets['Actions_Prob'] = probos
    return infosets, abs_infosets

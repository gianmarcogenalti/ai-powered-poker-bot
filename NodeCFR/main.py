import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import Utilities as U
from NodeCFR.CounterfactualRegretMinimizationBase import *
from NodeCFR.ChanceSamplingCFR import *
from NodeCFR.VanillaCFR import *

def nodecfr(nodes, infosets, abs_infosets, game, method = 'public_chance', T = 1000, verbose = False):
# Enriching the nodes and abstract infosets dataframe
    U.update_natureprob(nodes)
    U.maptoclust(infosets, abs_infosets)
    U.abstractnodes(nodes, abs_infosets, infosets)
    U.abstractsons(nodes, abs_infosets, infosets)
    U.abstractdads(abs_infosets)
    U.abs_depth(abs_infosets)
    U.nodetoclust(nodes, infosets, abs_infosets)
    abs_infosets = U.chance_to_infoset(nodes, abs_infosets)
    if method == 'public_chance':
        chance_sampling_cfr = ChanceSamplingCFR(nodes)
        chance_sampling_cfr.run(iterations = T)
        chance_sampling_cfr.compute_nash_equilibrium()
        #chance_sampling_cfr.print_output(game, method, infosets)
        U.get_back(infosets, abs_infosets, chance_sampling_cfr.nash_equilibrium)

    elif method == 'vanilla':
        vanilla_cfr = VanillaCFR(nodes)
        vanilla_cfr.run(iterations = T)
        vanilla_cfr.compute_nash_equilibrium()
        #vanilla_cfr.print_output(game, method, infosets)
        U.get_back(infosets, abs_infosets, vanilla_cfr.nash_equilibrium)
        #abs_infosets['Actions_Prob'] = chance_sampling_cfr.nash_equilibrium
    return infosets, abs_infosets

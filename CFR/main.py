import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import Utilities as U
from CFR.Vanilla_Gamer import *
from CFR.MC_Gamer import *

# Choose game:
def cfr(nodes, infosets, abs_infosets, game, method = 'vanilla', T = 100, verbose = False):
# Enriching the nodes and abstract infosets dataframe
    U.update_natureprob(nodes)
    U.maptoclust(infosets, abs_infosets)
    U.abstractnodes(nodes, abs_infosets, infosets)
    U.abstractsons(nodes, abs_infosets, infosets)
    U.abstractdads(abs_infosets)
    U.abs_depth(abs_infosets)

    if method == 'vanilla':
        monkey = Vanilla_Gamer(abs_infosets, nodes, verbose)
        monkey.train(T)
        monkey.compute_nash()
        #monkey.print_output(game, infosets)
        #abs_infosets['Actions_Prob'] = monkey.nash_equilibrium
        U.get_back(infosets, abs_infosets, monkey.nash_equilibrium)

    if method == 'montecarlo':
        frogs = MC_Gamer(abs_infosets, nodes, verbose)
        frogs.train(T)
        frogs.compute_nash()
        frogs.print_output(game, infosets)
        abs_infosets['Actions_Prob'] = frogs.nash_equilibrium
        U.get_back(infosets, abs_infosets, frogs.nash_equilibrium)

    return infosets, abs_infosets

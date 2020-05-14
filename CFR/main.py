from CFR.abstractpreparation import *
from CFR.Vanilla_Gamer import *
from CFR.MC_Gamer import *

# Choose game:
def cfr(nodes, infosets, abs_infosets, game, method = 'vanilla', T = 100, verbose = False):
# Enriching the nodes and abstract infosets dataframe
    update_nodeprob(nodes)
    maptoclust(infosets, abs_infosets)
    abstractnodes(nodes, abs_infosets, infosets)
    abstractsons(nodes, abs_infosets, infosets)
    abstractdads(abs_infosets)
    abs_depth(abs_infosets)

    if method == 'vanilla':
        monkey = Vanilla_Gamer(abs_infosets, nodes, verbose)
        monkey.train(T)
        monkey.compute_nash()
        monkey.print_output(game, infosets)
        abs_infosets['Actions_Prob'] = monkey.nash_equilibrium
        get_back(infosets, abs_infosets, monkey.nash_equilibrium)
        '''
        filename = game + "_infosets.csv"
        filename2 = game + "_blueprint.csv"
        infosets.to_csv(filename, index = False, header = True, escapechar=' ')
        abs_infosets.to_csv(filename2, index = False, header = True, escapechar=' ')
        '''

    if method == 'montecarlo':
        frogs = MC_Gamer(abs_infosets, nodes, verbose)
        frogs.train(T)
        frogs.compute_nash()
        frogs.print_output(game, infosets)
        abs_infosets['Actions_Prob'] = frogs.nash_equilibrium
        get_back(infosets, abs_infosets, frogs.nash_equilibrium)

    return infosets, abs_infosets

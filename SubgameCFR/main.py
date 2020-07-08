import Utilities as U
from SubgameCFR.ChanceSamplingCFR import *
from SubgameCFR.VanillaCFR import *
from SubgameCFR.VanillaCFRPlus import *

def subgameresolver(nodes, infosets, abs_infosets, roots, leaves,players, method = 'public_chance', T = 100):
    '''
    ################################################################################
    environment = {"game" : "leduc5", "T" : 100, "method" : 'vanilla'}
    ################################################################################

    vanilla_cfr = VanillaCFR(nodes)
    vanilla_cfr.run(iterations = environment["T"])
    vanilla_cfr.compute_nash_equilibrium()
    vanilla_cfr.print_output(environment["game"], environment["method"], infosets)

    get_back(infosets, vanilla_cfr.nash_equilibrium)
    filename = "vanilla_" + "nash_"+ game + "_infosets.csv"
    infosets.to_csv(filename, index = False, header = True, escapechar=' ')

    get_back(infosets, vanilla_cfr.sigma)
    filename = "vanilla_" + "sigma_"+ game + "_infosets.csv"
    infosets.to_csv(filename, index = False, header = True, escapechar=' ')
    '''
################################################################################
#environment = {"game" : "leduc5", "T" : 10000, "method" : 'public_chance'}
################################################################################
    if method == 'public_chance':
        output = dict()
        for it in range(len(roots)):
            chance_sampling_cfr = ChanceSamplingCFR(nodes,abs_infosets, roots, leaves, players,it)
            chance_sampling_cfr.run(iterations = T)
            chance_sampling_cfr.compute_nash_equilibrium()
            for t in roots[it]:
                output.update({str(t) : chance_sampling_cfr.nash_equilibrium[t]})
        return output
#chance_sampling_cfr.print_output(environment["game"], environment["method"], infosets)
    '''
    get_back(infosets, chance_sampling_cfr.nash_equilibrium)
    filename = environment["method"] + "_nash_"+ game + "_infosets.csv"
    infosets.to_csv(filename, index = False, header = True, escapechar=' ')

    get_back(infosets, chance_sampling_cfr.nash_equilibrium)
    filename = environment["method"] + "_sigma_"+ game + "_infosets.csv"
    infosets.to_csv(filename, index = False, header = True, escapechar=' ')
    '''
    '''
    ################################################################################
    environment = {"game" : "leduc5", "T" : 100, "method" : 'vanilla_plus'}
    ################################################################################

    vanilla_cfr_plus = VanillaCFRPlus(nodes)
    vanilla_cfr_plus.run(iterations = environment["T"])
    vanilla_cfr_plus.compute_nash_equilibrium()
    vanilla_cfr_plus.print_output(environment["game"], environment["method"], infosets)

    get_back(infosets, vanilla_cfr_plus.nash_equilibrium)
    filename = environment["method"] + "_nash_" + game + "_infosets.csv"
    infosets.to_csv(filename, index = False, header = True, escapechar=' ')

    get_back(infosets, vanilla_cfr_plus.sigma)
    filename = environment["method"] + "_sigma_"+ game + "_infosets.csv"
    infosets.to_csv(filename, index = False, header = True, escapechar=' ')
    '''

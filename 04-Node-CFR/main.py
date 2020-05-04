from loaddata4 import *
from abstractpreparation2 import *
from ChanceSamplingCFR import *
from VanillaCFR import *

game = "leduc3"
# Loads the csv and gets the proper infosets
infosets = loadinfosets(game)
abs_infosets = loadabstract(game)
nodes    = loadnodes(game)
# Enriching the nodes and abstract infosets dataframe
maptoclust(infosets, abs_infosets)
nodetoclust(nodes, infosets, abs_infosets)
abs_infosets = chance_to_infoset(nodes, abs_infosets)

################################################################################
environment = {"game" : "leduc3", "T" : 100, "method" : 'vanilla'}
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

################################################################################
environment = {"game" : "leduc3", "T" : 10000, "method" : 'public_chance'}
################################################################################
chance_sampling_cfr = ChanceSamplingCFR(nodes)
chance_sampling_cfr.run(iterations = environment["T"])
chance_sampling_cfr.compute_nash_equilibrium()
chance_sampling_cfr.print_output(environment["game"], environment["method"], infosets)

get_back(infosets, chance_sampling_cfr.nash_equilibrium)
filename = "public_chance_" + "nash_"+ game + "_infosets.csv"
infosets.to_csv(filename, index = False, header = True, escapechar=' ')

get_back(infosets, chance_sampling_cfr.nash_equilibrium)
filename = "public_chance_" + "sigma_"+ game + "_infosets.csv"
infosets.to_csv(filename, index = False, header = True, escapechar=' ')

################################################################################

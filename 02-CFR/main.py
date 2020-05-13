from loaddata2 import *
from abstractpreparation import *
from Vanilla_Gamer import *
from MC_Gamer import *
from trees2 import *

# Choose game:

game = "leduc5"

# Loads the csv and gets the proper infosets
infosets = loadinfosets(game)
abs_infosets = loadabstract(game)
nodes    = loadnodes(game)
# Enriching the nodes and abstract infosets dataframe
update_nodeprob(nodes)
maptoclust(infosets, abs_infosets)
abstractnodes(nodes, abs_infosets, infosets)
abstractsons(nodes, abs_infosets, infosets)
abstractdads(abs_infosets)
abs_depth(abs_infosets)
'''
for i in range(len(abs_infosets.index)):
    print(abs_infosets.Depth[i], abs_infosets.Player[i])
'''
# Environment set
T = 100

method = 'vanilla'
monkey = Vanilla_Gamer(abs_infosets, nodes)
monkey.train(T)
monkey.compute_nash()
#print(monkey.nash_equilibrium)
monkey.print_output(game, infosets)
#print(monkey.strategies)
'''
method = 'montecarlo'
frogs = MC_Gamer(abs_infosets, nodes)
print(frogs.proxy)
frogs.train(T)
frogs.compute_nash()
print(frogs.nash_equilibrium)
'''



## Tree rendering

#nodestree(nodes, "probability")
abs_infosets['Actions_Prob'] = monkey.nash_equilibrium
get_back(infosets, monkey.nash_equilibrium)
filename = game + "_infosets.csv"
filename2 = game + "_blueprint.csv"
infosets.to_csv(filename, index = False, header = True, escapechar=' ')
abs_infosets.to_csv(filename2, index = False, header = True, escapechar=' ')

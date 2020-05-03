from loaddata2 import *
from abstractpreparation import *
#from Vanilla_Gamer import *
#from MC_Gamer import *
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

for i in range(len(abs_infosets.index)):
    print(abs_infosets.Depth[i], abs_infosets.Player[i])
'''
# Environment set
T = 10

method = 'vanilla'
monkey = Vanilla_Gamer(abs_infosets, nodes)
monkey.train(T)
monkey.print_output(game, infosets)
#print(monkey.strategies)

method = 'montecarlo'
frogs = MC_Gamer(abs_infosets, nodes)
frogs.waterlilies_select(2)
print(frogs.proxy)
frogs.train(T)
print(frogs.strategies)




## Tree rendering

#nodestree(nodes, "probability")

get_back(infosets, monkey.strategies)
filename = game + "_infosets.csv"
infosets.to_csv(filename, index = False, header = True, escapechar=' ')
'''

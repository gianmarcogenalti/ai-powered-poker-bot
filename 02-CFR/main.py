from loaddata2 import *
from abstractpreparation import *
from Vanilla_Gamer import *
from trees2 import *

# Choose game:

game = "leduc3"

# Loads the csv and gets the proper infosets
infosets = loadinfosets(game)
abs_infosets = loadabstract(game)
nodes    = loadnodes(game)

# Enriching the nodes and abstract infosets dataframe
update_nodeprob(nodes)
maptoclust(infosets, abs_infosets)
abstractnodes(nodes, abs_infosets, infosets)
abstractsons(nodes, abs_infosets, infosets)
'''
for i in range(len(abs_infosets.index)):
    print(abs_infosets.Direct_Sons[i])
'''

# Environment set
T = 10
method = 'vanilla'
monkey = Vanilla_Gamer(abs_infosets, nodes)
monkey.recursive_probs_abstract_call(monkey.infosets.index[30])
for i in range(len(monkey.infosets.index)):
    print(monkey.infosets.Probability[i])

## Tree rendering

#nodestree(nodes, "probability")

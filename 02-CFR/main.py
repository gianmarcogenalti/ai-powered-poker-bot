from loaddata2 import *
from abstractpreparation import *
#from Vanilla_Gamer import *
from Node_Gamer import *
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
# Environment set
T = 10
method = 'vanilla'
nodes.Probability = [[] for _ in range(len(nodes.index))]
nodes.Probability[-1] = 1.0
monkey = Node_Gamer(abs_infosets, nodes)
monkey.recursive_probs(nodes.index[-1])

'''
## Tree rendering

#nodestree(nodes, "probability")

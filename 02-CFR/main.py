from loaddata2 import *
from abstractpreparation import *
from Vanilla_Gamer import *
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
#print(nodes.Nature_Prob)
abstractnodes(nodes, abs_infosets, infosets)
abstractsons(nodes, abs_infosets)
#for index,row in abs_infosets.iterrows():
#    print(row.Nature_Weight)
monkey = Vanilla_Gamer(abs_infosets, nodes)
roots = abs_infosets.index[abs_infosets.Depth == 1]
for startingidx in roots:
    monkey.recursive_probs_abstract_call(startingidx, init = True)
    print(1)
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

nodestree(nodes, "probability")

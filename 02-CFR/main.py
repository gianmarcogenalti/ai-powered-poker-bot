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

histoparents(abs_infosets)
abstractnodes(nodes, abs_infosets, infosets)
print(nodes)
print(nodes.Payoff_Vector_P1)
print(abs_infosets.Index_Members)

# Environment set
T = 10
method = 'vanilla'

print(nodes.Payoff_Vector_P1)
gamer = Vanilla_Gamer(abs_infosets, nodes)
print(gamer.nodes)
gamer.tree_drop()
print(gamer.recursive_payoff(2))
#gamer.update_abstract(0, [0.5,0.5])
#nodestree(gamer.nodes, "payoffs")

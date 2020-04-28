from loaddata2 import *
from abstractpreparation import *
from Vanilla_Gamer import *

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

# Environment set
T = 10
method = 'vanilla'

print(nodes.Payoff_Vector_P1)
gamer = Vanilla_Gamer(abs_infosets, nodes)
gamer.tree_drop()
gamer.update_abstract(0, [0.5,0.5])
print(gamer.nodes)

from loaddata2 import *
from abstractpreparation import *
from TreePartitioner import *
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

part = TreePartitioner(abs_infosets)
part.coparents()
print(part.coroots)

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

maptoclust(infosets, abs_infosets)
abstractnodes(nodes, abs_infosets, infosets)
nodeblueprint(nodes,abs_infosets)
update_nodeprob(nodes)
print(nodes.Probability)
abstractsons(nodes, infosets, infosets)
abstractdads(abs_infosets)
abs_depth(abs_infosets)
print(abs_infosets.Actions_Prob)

part = TreePartitioner(abs_infosets)
part.coparents()
part.infotonodes()
print('Parents: ',part.info_roots)
print('Sons: ', part.info_sons)
#print('Node Parents: ', part.node_roots)
#print('Node Sons: ', part.node_sons)

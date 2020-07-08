
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import Utilities as U
from Subgames.TreePartitioner import *
# Choose game:
def subgamegeneration(nodes, infosets, abs_infosets, limited = True):

    U.absnature(nodes,infosets,abs_infosets)
    U.nodetoclust(nodes,infosets,abs_infosets)
    U.nodeblueprint(nodes,abs_infosets)
    U.update_nodeprob(nodes)

    part = TreePartitioner(abs_infosets, depth_lim = limited, max_depth = 5)
    part.subgamegenerator()
    nodes  = part.chanceroot(nodes)
    abs_infosets = U.chance_to_infoset(nodes, abs_infosets)
    #subgames = part.info_subgames
    roots = part.info_roots
    leaves = part.info_leaves
    players = part.subgameplayer
    #print(part.info_subgames)
    #print(part.info_roots)
    #print(part.info_leaves)
    #U.prob_leaf(nodes)
    return nodes, abs_infosets, roots, leaves, players

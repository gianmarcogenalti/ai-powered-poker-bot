import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import Utilities as U
#from loaddata2 import *
from Subgames.TreePartitioner import *
# Choose game:
def subgameresolver(nodes, infosets, abs_infosets):
    U.nodeblueprint(nodes,abs_infosets)
    U.absnature(nodes,infosets,abs_infosets)
    #abs_infosets = U.chance_to_infoset(nodes, abs_infosets)
    #print(abs_infosets.Actions_Prob)

    part = TreePartitioner(abs_infosets, depth_lim = True, max_depth = 5)
    part.subgamegenerator()
    print(part.info_subgames)
    print(part.info_roots)

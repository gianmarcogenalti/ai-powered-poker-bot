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
    #print(abs_infosets.Actions_Prob)

    part = TreePartitioner(abs_infosets)
    part.coparents()
    part.infotonodes()
    #print('Parents: ',part.info_roots)
    #print('Sons: ', part.info_sons)
    #print('Node Parents: ', part.node_roots)
    #print('Node Sons: ', part.node_sons)

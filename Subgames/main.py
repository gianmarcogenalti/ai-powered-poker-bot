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
    
    nodes.Expected_Payoff = [0 for i in range(len(nodes))]
    nodes.BPProbability = [0 for i in range(len(nodes))]
    def recursivethings(icn):
        if nodes.Direct_Sons[icn] != -1:
            for ids in range(len(nodes.Direct_Sons[icn])):
                ds = nodes.Direct_Sons[icn][ids]
                ap = nodes.Actions_Prob[icn][ids]
                nodes.BPProbability[ds] += ap * nodes.BPProbability[icn]
                nodes.Expected_Payoff[icn] += ap * recursivethings(ds)
        else:
            current_node.Expected_Payoff = nodes.Payoff_P1[icn]
        return nodes.Expected_Payoff[icn]
    start = nodes.iloc[nodes.Dad == -1]
    nodes.BPProbability[start] = 1
    recursivethings(start)

    part = TreePartitioner(abs_infosets, depth_lim = True, max_depth = 5)
    part.subgamegenerator()
    print(part.info_subgames)
    print(part.info_roots)

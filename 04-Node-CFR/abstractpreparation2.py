import re
import pandas as pd
import numpy as np

def nodetoclust(nodes, infosets, abs_infosets):
    map = [[] for _ in range(len(nodes.index))]
    for index, row in nodes.iterrows():
        if row.Type == 'N':
            maptoinf = row.Map
            maptoclust = infosets.Map_Clust[maptoinf][0]
        else:
            maptoclust = -999999
        #print(maptoclust)
        map[index]= (maptoclust)

    nodes['Abs_Map'] = map

def maptoclust(infosets, abs_infosets):
    map = [[] for _ in range(len(infosets.index))]
    for index,row in abs_infosets.iterrows():
        for inf in row.Map:
            map[inf].append(index)
        #
    #
    infosets['Map_Clust'] = map

def chance_to_infoset(nodes, abs_infosets):
    chances = nodes[nodes.Type == 'C']
    nmax = len(abs_infosets.index)
    counter = 0
    for index,crow in chances.iterrows():
        nodes.Abs_Map[index] = nmax + counter
        counter += 1
        cdf = pd.DataFrame([index], columns = ['Map'])
        abs_infosets = abs_infosets.append(cdf, ignore_index=True)

    return abs_infosets

def get_back(infosets, strategies):
    act_probs = []
    for index,row in infosets.iterrows():
        strats = strategies[row.Map_Clust[0]]
        toapp = []
        for a in row.Actions:
            toapp.append(strats[a])
        act_probs.append(toapp)
    infosets['Actions_Prob'] = act_probs

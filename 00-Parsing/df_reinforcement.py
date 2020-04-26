from hierarchy import *
from txtparsing import nodeiscomp, getnodedepth
import re

## Utilities that add columns to the original dataframes

def isplayers(infosets, nodes):
    finalp = []
    for index,row in infosets.iterrows():
        memb = row.Index_Members[0]
        finalp.append(nodes.Player[memb])
    infosets['Player'] = finalp

def descendents(infosets) :
    descendent = []
    for i in range(len(infosets)) :
        descendent.append(sons(infosets, i))
    #
    infosets['Sons'] = descendent

def alldescendents(infosets) :
    descendent = []
    for i in range(len(infosets)) :
        descendent.append(allsons(infosets, i))
        #
    infosets['All_Sons'] = descendent

def antenates(infosets) :
    antenate = []
    for i in range(len(infosets)) :
        antenate.append(parents(infosets, i))
    #
    infosets['Parents'] = antenate

def maptois(nodes, infosets) :
    map = [0] * len(nodes.index)
    for nindex, nrow in nodes.iterrows():
        if nrow.Type == 'N':
            player = nrow['Player']
            if len(infosets.index.values[nodeiscomp(nrow.History, infosets.History, player)]) > 0:
                i = infosets.index.values[nodeiscomp(nrow.History, infosets.History, player)][0]
                map[nindex] = i
        else:
            map[nindex] = -1
    #
    nodes['Map'] = map

def indexmembers(infosets, nodes) :
    ixmembers = [[] for _ in range(len(infosets.index))]
    for index, row in nodes.iterrows() :
        if row.Type == 'N':
            i = row['Map']
            ixmembers[i].append(index)
    #
    infosets['Index_Members'] = ixmembers

def nodesdepth(nodes):
    depth = []
    for hist in nodes.History:
        depth.append(getnodedepth(hist))
    nodes['Depth'] = depth

def payoffdescendents(nodes, infosets = None):
    descendent = [[] for _ in range(len(nodes.index))]
    po1 = [[] for _ in range(len(nodes.index))]
    #nodesdad = [[] for _ in range(len(nodes.index))]
    root = nodes.iloc[nodes.index[nodes.History == "/"].tolist()[0]]
    def recursivesons(dad): ##improved
        if dad.Type == 'L':
            po1[dad.name] = [dad.Payoff_P1]
            return [[], [dad.Payoff_P1]]

        if dad.Player == 1:
            player = '/P1:'
        else:
            if dad.Player == 2:
                player = '/P2:'
            else:
                player = '/C:'

        if(dad.History == '/'):
            for action in dad.Actions:
                son1 = '/C:' + action
                son = nodes.iloc[nodes.index[nodes.History == son1].tolist()[0]]
                idxson = son.name
                #nodesdad[idxson] = int(dad.name)
                outlist = recursivesons(son)
                descendent[dad.name] = descendent[dad.name] + outlist[0] + [idxson]
                po1[dad.name] = po1[dad.name] + outlist[1]
        else:
            for action in dad.Actions:
                son1 = dad.History + player + action
                son = nodes.iloc[nodes.index[nodes.History == son1].tolist()[0]]
                idxson = son.name
                #nodesdad[idxson] = int(dad.name)
                outlist = recursivesons(son)
                descendent[dad.name] = descendent[dad.name] + outlist[0] + [idxson]
                po1[dad.name] = po1[dad.name] + outlist[1]

        return descendent[dad.name],po1[dad.name]

    recursivesons(root)
    nodes['Sons'] = descendent
    nodes['Payoff_Vector_P1'] = po1
    #nodes['Dad'] = nodesdad

def ispayoffs(infosets, nodes):
    ispo1 = [[] for _ in range(len(infosets.index))]
    for index,row in infosets.iterrows():
        for i in row.Index_Members:
            ispo1[index] += nodes.Payoff_Vector_P1[i]
        #
    #
    infosets['Payoff_Vector_P1'] = ispo1

def nodeantenates(nodes) : ##improved
    antenate = [[] for _ in range(len(nodes.index))]
    for index,row in nodes.iterrows() :
        for sindex in row['Sons'] :
            antenate[sindex].append(index)
        #
    #
    nodes['Parents'] = antenate


def isactions(infosets, nodes) :
    actions =  []
    for index,row in infosets.iterrows() :
        map = row.Index_Members[0]
        actions.append(nodes.Actions[map])
    #
    infosets['Actions'] = actions

def directparent(nodes, infosets):
    dads = []
    isdads = [[] for _ in range(len(infosets.index))]
    for index,row in nodes.iterrows():
        if row.History != '/':
            for parent in row.Parents:
                if nodes.Depth[parent] == row.Depth - 1:
                    dads.append(parent)
                    if nodes.History[parent] == '/':
                        isdads[row.Map] = -1
                    if row.Type != 'C':
                        if nodes.Type[parent] != 'C':
                            if not nodes.Map[parent] in isdads[row.Map]:
                                if row.Map != -1:
                                    isdads[row.Map].append(nodes.Map[parent])
                                else:
                                    print('Error 3')
                        if nodes.Type[parent] == 'C' and nodes.History[parent] != '/':
                            if row.Map != -1:
                                isdads[row.Map] = -2
                            else:
                                print('Error 2')


                #
            #
        else:
            dads.append(-1)
    #
    nodes['Dad'] = dads
    infosets['Dad'] = isdads
    for index,row in infosets.iterrows():
        if infosets.Dad[index] == -2:
            infosets.Dad[index] = []
            for i in row.Index_Members:
                if nodes.Type[nodes.Dad[i]] == 'C':
                    grandpa = nodes.Dad[nodes.Dad[i]]
                    isgrandpa = nodes.Map[grandpa]
                    if isgrandpa != -1:
                        if not isgrandpa in infosets.Dad[index]:
                            infosets.Dad[index].append(isgrandpa)
                    else:
                        print('Error')


def directsons(nodes):
    direct_sons = []
    for index,row in nodes.iterrows():
        sons = []
        if row.Type != 'L':
            for action in row.Actions:
                if row.History == '/':
                    hist = '/C:' + action
                else:
                    if row.Player == 0:
                        hist = row.History + '/C:' + action
                    if row.Player == 1:
                        hist = row.History + '/P1:' + action
                    if row.Player == 2:
                        hist = row.History + '/P2:' + action
                #
                candidates = nodes[nodes.Depth == row.Depth +1]
                sons.append(int(candidates.index.values[candidates.History == hist]))
            #
            direct_sons.append(sons)
        else:
            direct_sons.append(-1)
    #
    nodes['Direct_Sons'] = direct_sons
'''
def isdirectsons(infosets,nodes):
    direct_sons = []
    for index, row in infosets.iterrows():
        for i in row.Index_Members:
            ds = []
            for son in nodes.Direct_Sons[i]:


def isdirectsons(infosets):
    direct_sons = []
    for index,row in infosets.iterrows():
        sons = []
        for action in row.Actions:
            if row.Player == 1:
                hist = row.History + '/P1:' + action
            if row.Player == 2:
                hist = row.History + '/P2:' + action
                #
                candidates = nodes[nodes.Depth == row.Depth +1]
                sons.append(int(candidates.index.values[candidates.History == hist]))
            #
            direct_sons.append(sons)
        else:
            direct_sons.append(-1)
    #
    nodes['Direct_Sons'] = direct_sons
'''

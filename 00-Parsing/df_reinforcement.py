from hierarchy import *
from txtparsing import nodeiscomp, getnodedepth
import re

## Utilities that add columns to the original dataframes

def payoffvectors(infosets,nodes):
    pv1 = []
    terminals = nodes[nodes.Type == 'L']
    #pv2 = [[] for _ in range(len(infosets.index))]
    for index,row in infosets.iterrows():
        for member in row.Members:
            payoff = []
            for tindex,terminal in terminals.iterrows():
                if terminal.History.find(member) != -1:
                    c1 = terminal.Payoff_P1
                    #c2 = -c1
                    payoff.append(c1)
                #
            #
        #
        pv1.append(payoff)
    #
    infosets['Payoff_Vector_P1'] = pv1


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
'''
def nodedescendents(nodes = None, leaf = None) : ##improved
    descendent = [[] for _ in range(len(nodes.index))]
    for index,row in nodes[nodes.Type == 'L'].iterrows() :
        if(row.History == '/'):
            descendent[index] = nodes.index.values
        else:
            nd = nodes.where(nodes.History.str.find(row.History + '/') != -1)
            nd = nd.dropna()
            descendent[index] = nd.index.values
    #
    nodes['Sons'] = descendent
'''
def nodedescendents(nodes):
    globalnodes = nodes
    descendent = [[] for _ in range(len(nodes.index))]
    root = nodes[nodes.History == '/']
    def recursivesons(dad): ##improved
        if dad.Type == 'L':
            return []
        if dad.Player == 1:
            player = '/P1:'
        if dad.Player == 2:
            player = '/P2:'
        else:
            player = '/C:'
        if(dad.History == '/'):
            for action in root.Actions:
                son = '/C:' + action
                son = nodes[nodes.History == son]
                idxson = son.index
                descendent[dad.index].append(recursivesons(son), idxson)
        else:
            for action in root.Actions:
                son = dad.History + player  + action
                son = nodes[nodes.History == son]
                idxson = son.index
                descendent[dad.index].append(recursivesons(son), idxson)

        return descendent[dad.index]

    recursivesons(root)
    print(descendent)

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

def directparent(nodes):
    dads = []
    for index,row in nodes.iterrows():
        if row.History != '/':
            for parent in row.Parents:
                if nodes.Depth[parent] == row.Depth - 1:
                    dads.append(parent)
                #
            #
        else:
            dads.append(-1)
    #
    nodes['Dad'] = dads

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

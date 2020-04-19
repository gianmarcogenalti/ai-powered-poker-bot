from hierarchy import *
from txtparsing import nodeiscomp
import re

## Utilities that add columns to the original dataframes

def payoffvectors(infosets, terminals) :
    finalpv1 = []
    finalpv2 = []
    ##modpv1 = []
    #modpv2 = []
    for info in infosets['Members']:
        pv1 = []
        pv2 = []
        #mod1 = 0
        #mod2 = 0
        for member in info :
            counter = 0
            for terminal in terminals['History'] :
                if(terminal.find(member) != -1) :
                    c1 = terminals['Payoff'][counter][0]
                    c2 = terminals['Payoff'][counter][1]
                    pv1.append(c1)
                    ###mod1 = mod1 + c1*c1
                    pv2.append(c2)
                    ##mod2 = mod2 + c2*c2
                counter = counter + 1
            #end for terminals
        #end for member
        finalpv1.append(pv1)
        #modpv1.append(mod1)
        finalpv2.append(pv2)
        #modpv2.append(mod2)
        #print(finalpv1)
        #print(len(finalpv1))
    #end for info
    infosets['Payoff Vector P1'] = finalpv1
    #infosets['Payoff Modulus P1'] = modpv1
    infosets['Payoff Vector P2'] = finalpv2
    #infosets['Payoff Modulus P2'] = modpv2

def isplayers(infosets, nonterminals) :
    finalp = []
    for member in infosets['Members'] :
        counter = 0
        for nonterminal in nonterminals['History'] :
            if(nonterminal == member[0]):
                finalp.append(nonterminals['Player'][counter])
            counter = counter + 1
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
        player = nrow['Player']
        if len(infosets.index.values[nodeiscomp(nrow.History, infosets.History, player)]) > 0:
            i = infosets.index.values[nodeiscomp(nrow.History, infosets.History, player)][0]
            map[nindex] = i
    #
    nodes['Map'] = map

def indexmembers(infosets, nodes) :
    ixmembers = [[] for _ in range(len(infosets.index))]
    for index, row in nodes.iterrows() :
        i = row['Map']
        ixmembers[i].append(index)
    #
    infosets['Index_Members'] = ixmembers

def nodedepth(nodes, infosets) :
    depth = [0] * len(nodes.index)
    for index, row in nodes.iterrows() :
        i = row['Map']
        depth[index] = infosets['Depth'][i]
    #
    nodes['Depth'] = depth

def nodedescendents(nodes) : ##improved
    descendent = [[] for _ in range(len(nodes.index))]
    for index,row in nodes.iterrows() :
        nd = nodes.where(nodes.History.str.find(row.History + '/') != -1)
        nd = nd.dropna()
        descendent[index] = nd.index.values
    #
    nodes['Sons'] = descendent

def nodeantenates(nodes) : ##improved
    antenate = [[] for _ in range(len(nodes.index))]
    for index,row in nodes.iterrows() :
        for sindex in row['Sons'] :
            antenate[sindex].append(index)
        #
    #
    nodes['Parents'] = antenate


def isactions(infosets, nodes) :
    actions =  [[] for _ in range(len(infosets.index))]
    for index,row in infosets.iterrows() :
        map = row['Index_Members'][0]
        actions[index] = nodes.Actions[map]
    #
    infosets['Actions'] = actions

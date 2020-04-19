import pandas as pd
import numpy as np
from utilities import *
import re

# MERGES INFOSETS WITHOUT INFORMATION LOSS

# list of available games
kuhn = "kuhn"
l3 = "leduc3"
l5 = "leduc5"

# choose the game to cluster and loads the cvs as df
game = l3
infosets, terminals, nonterminals, chances = loadcsvs(game)

# simplifies its history creating a structure made out of flags
infosets['Structure'] = createstructure(infosets['History'])

# infosetsMerger rows will be the sets of infosets that are going to be merged together without loss of information 
infosetsMerger = list()
rp = realParents(infosets)

# select depth and cluster without loss of information
for depth in range(1,max(infosets['Depth'])+1):
    print("depth #"+str(depth))
    # cycle between them and check wether they are mergeable for each depth
    infosetsMerger = fastMerger(infosetsMerger,infosets,inddepth(infosets,depth),rp)
   
# Maps the initial rows of infosets into the index of row of the final merged infosets
infosets['Map'] = mapinfosets(infosets,infosetsMerger) # from old to new

# builds the output dataFrame
infoMerged = pd.DataFrame(columns=['Map','Depth','Payoff Vector P1','Player','Sons','Parents','Structure'])
infoMerged['Map'] = infosetsMerger # from new to old

# builds the remaining output dataFrame's columns
depths = []
payoffs = []
players = []
structures = []
parents = []
sons = []
for im in infosetsMerger :
    depths.append(infosets['Depth'][im[0]])
    payoffs.append(infosets['Payoff Vector P1'][im[0]])
    players.append(infosets['Player'][im[0]])
    structures.append(infosets['Structure'][im[0]])
    # gets the new indexes of the parents
    parentsnow = []
    for iml in im :
        if infosets['Parents'][iml] != [] :
            for par in infosets['Parents'][iml]: # old index
                if not infosets['Map'][par] in parentsnow:
                    parentsnow.append(infosets['Map'][par]) # new index
    parents.append(parentsnow)
    # gets the new indexes of the sons
    sonsnow = []
    for iml in im :
        if infosets['Sons'][iml] != []: # there are sons
            for son in infosets['Sons'][iml]:
                if not infosets['Map'][son] in sonsnow:
                    sonsnow.append(infosets['Map'][son])
    sons.append(sonsnow)

# inserts the columns
infoMerged['Depth'] = depths
infoMerged['Payoff Vector P1'] = payoffs
infoMerged['Player'] = players
infoMerged['Structure'] = structures
infoMerged['Parents'] = parents
infoMerged['Sons'] = sons

# returns and saves the dataFrame
print(infoMerged.head)
infoMerged.to_csv("..\\Import_files\\ph1_"+game+".csv", index = False, header = True)
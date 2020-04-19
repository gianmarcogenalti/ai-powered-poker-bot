import pandas as pd
import numpy as np
from utilities import *
import re
import math

# CLUSTERS INFOSETS WITH INFORMATION LOSS

# list of available games
kuhn = "kuhn"
l3 = "leduc3"
l5 = "leduc5"

# choose the game to cluster and loads the cvs as df
game = l5
infosets, terminals, nonterminals, chances = loadcsvs(game)
# NOTE: infosets has a different number of records from the others
# some infosets were already merged in the pre clustering phase

# infosetsMerger rows will be the sets of infosets that are going to be clustered 
infosetsMerger = list()
infosetsMergerPay = list()
rp = realParents(infosets)

# select depth and cluster without loss of information
for depth in range(1,max(infosets['Depth'])+1):
    print("##  ## depth #"+str(depth))
    # cycle between them and check wether they are clusterable for each depth
    infosetsMerger, clustPay = fastClusterer(infosetsMerger,infosets,inddepth(infosets,depth),rp)
    [infosetsMergerPay.append(cp) for cp in clustPay]
    
    
   
print(len(infosetsMerger))
print(len(infosetsMergerPay))
#print(infosetsMergerPay)
#print(infosets.head)
# Maps the initial rows of infosets into the index of row of the final merged infosets

# builds the output dataFrame
infoMerged = pd.DataFrame(columns=['MapPh1','Map','Depth','Payoff Vector P1','Player','Sons','Parents','Structure','Index_Members','Actions','Actions_Prob','Probabilities'])

# Imports original Index_Members, Actions, Actions_Prob, Probabilities in the proper place
folderpath = "..\\Import-files\\"
startingInfosets = pd.read_csv(folderpath + game + "_infosets.csv", dtype={'History':str,'Members':str,'Depth':int,'Payoff Vector P1':str,'Payoff Vector P2':str,'Player':int,'Sons':str,'Parents':str,'Index_Members':str,'Actions':str,'Actions_Prob':str,'Probabilities':float})
startingInfosets['Index_Members'] = makeArrayInt(startingInfosets['Index_Members']) # int
startingInfosets['Actions'] = makeArray(startingInfosets['Actions']) # string
startingInfosets['Actions_Prob'] = makeArrayFloat(startingInfosets['Actions_Prob']) # float  


# builds the remaining output dataFrame's columns
depths = []
payoffs = []
players = []
structures = []
parents = []
sons = []
indexMembers = []
actions = []
actionsprob = []
probabilities = []
imi = 0
for im in infosetsMerger :
    if len(im) < 1 :
        infosetsMerger.remove(infosetsMerger[imi])
        infosetsMergerPay.remove(infosetsMergerPay[imi])
    imi += 1
    
maptooriginal = mapinfosetsoriginal(infosets,infosetsMerger)
infosets['MapPh1'] = mapinfosets(infosets,infosetsMerger)
print(infosetsMerger)
print(infosets['MapPh1'])
imi = 0
for im in infosetsMerger :
    depths.append(infosets['Depth'][im[0]]) # same depth in cluster
    players.append(infosets['Player'][im[0]]) # same player in cluster
    structures.append(infosets['Structure'][im[0]]) # same structure in cluster 
    # gets the new indexes of the parents
    parentsnow = list()
    for iml in im :
        if infosets['Parents'][iml] != [] : # there are parents
            for par in infosets['Parents'][iml]: # old index
                if not infosets['MapPh1'][par] in parentsnow:
                    parentsnow.append(infosets['MapPh1'][par]) # new index
    parents.append(parentsnow)  
    # gets the new indexes of the sons
    sonsnow = list()
    for iml in im :
        if infosets['Sons'][iml] != []: # there are sons
            for son in infosets['Sons'][iml]:
                if not infosets['MapPh1'][son] in sonsnow:
                    sonsnow.append(infosets['MapPh1'][son])
    sons.append(sonsnow)
    # Adds the elements of indexMembers
    indexMembersNow = list();
    for i1 in maptooriginal[imi] :
        indexMembersNow += startingInfosets['Index_Members'][i1]
    indexMembers.append(indexMembersNow)
    # Adds the elements of Actions
    actions.append(startingInfosets['Actions'][maptooriginal[imi][0]])
    # Adds the elements of ActionsProb
    actionsprob.append(startingInfosets['Actions_Prob'][maptooriginal[imi][0]])
    # Adds the elements of Probabilities
    probabilitiesnow = 0
    for i1 in maptooriginal[imi] :
        probabilitiesnow += startingInfosets['Probabilities'][i1]
    probabilities.append(probabilitiesnow)
    imi += 1
    
# inserts the columns
infoMerged['Depth'] = depths
infoMerged['Payoff Vector P1'] = infosetsMergerPay
infoMerged['Player'] = players
infoMerged['Structure'] = structures
infoMerged['Parents'] = parents
infoMerged['Sons'] = sons
infoMerged['MapPh1'] = infosetsMerger
infoMerged['Map'] = maptooriginal
infoMerged['Index_Members'] = indexMembers
infoMerged['Actions'] = actions
infoMerged['Actions_Prob'] = actionsprob
infoMerged['Probabilities'] = probabilities

# returns and saves the dataFrame
print(infoMerged.head)
infoMerged.to_csv("..\\Import-files\\clust_"+game+".csv", index = False, header = True)

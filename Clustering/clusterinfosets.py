import pandas as pd
import numpy as np
import time
import re
import math
from sklearn.cluster import KMeans
from Clustering.conditions import *

# Merges the infosets according to the specified mergeGroup
def mergeInfosets(infosets,mergeGroup,mergeGroupPay) :
    newinfosets = pd.DataFrame()

    #preallocates
    pdkeys = ['MapPh1','Map','History_Structure','Depth','Payoff','Player','Actions','Probability','Real_Parents']
    for pdkey in pdkeys :
        newinfosets[pdkey] = [[] for i in range(len(mergeGroup))]

    infosets['Map'] = infosets['MapPh1']

    # Transfers information
    for img in range(len(mergeGroup)) :
        newinfosets['MapPh1'][img] = mergeGroup[img]
        for imgi in mergeGroup[img]:
            infosets['MapPh1'][imgi] = img # Inverse map
        newinfosets['History_Structure'][img] = infosets['History_Structure'][mergeGroup[img][0]]
        newinfosets['Depth'][img] = infosets['Depth'][mergeGroup[img][0]]
        newinfosets['Player'][img] = infosets['Player'].loc[mergeGroup[img][0]]
        newinfosets['Actions'][img] = infosets['Actions'].loc[mergeGroup[img][0]]
        newinfosets['Probability'][img] = sum(infosets['Probability'].loc[mergeGroup[img]])

    # Updates final map
    if infosets['Map'][0] != [] :
        for maprow in range(len(newinfosets['MapPh1'])) :
            for maprowel in newinfosets['MapPh1'][maprow] :
                newinfosets['Map'][maprow] += infosets['Map'][maprowel]

    # Updates payoffs
    newinfosets['Payoff'] = mergeGroupPay

    # Updates Sons
    for img in range(len(mergeGroup)) :
        for imgi in mergeGroup[img] :
            par = infosets['Real_Parents'][imgi]
            for pari in par :
                parnmg = infosets['MapPh1'][pari]
                if not parnmg in newinfosets['Real_Parents'][img] :
                    newinfosets['Real_Parents'][img].append(parnmg)

    return newinfosets

def payoffAverage(toMerge,infosets) :
    payres = []
    for tm in toMerge :
        if len(tm) < 1 :
            payres.append([0])
        elif len(tm) == 1 :
            payres.append(infosets['Payoff'][tm[0]])
        else :
            sumnp = np.zeros(len(infosets['Payoff'][tm[0]]))
            for tm2 in tm :
                sumnp = np.add(sumnp, np.array(infosets['Payoff'][tm2], dtype=float))
            nptl = np.divide(sumnp,len(tm))
            payres.append(nptl.tolist())
    return payres

# Calls kmeans algorithm
def kmeanscall(toMerge,infosets,sizeofabstraction) :
    k = int(max(1,len(toMerge)-sum(sizeofabstraction < np.random.rand(len(toMerge),1))))
    #k = round(sizeofabstraction*len(toMerge))
    pv = list()
    [pv.append(infosets['Payoff'][mg]) for mg in toMerge]
    mg = np.array(pv)
    kmeans = KMeans(n_clusters=k, random_state=0).fit(mg)
    labs = kmeans.labels_
    clustGroup = list()
    [clustGroup.append(list()) for i in range(0,k)]
    ikml = 0
    for kml in labs :
        if toMerge[ikml] != [] :
            clustGroup[kml].append(toMerge[ikml])
        ikml += 1
    clustPay = payoffAverage(clustGroup,infosets)
    return clustGroup, clustPay

# Merges infosets into clusters
def cluster(infosets, infoloss, sizeofabstraction = 1) :

    # List of lists: inner lists are to be merged together
    mergeGroup = []
    mergeGroupPay = []

    # Updates the mergeGroup with the indexes at idxinfo (at same depth)
    def updateMergeGroup(idxinfo,mergeGroup,mergeGroupPay, sizeofabstraction = 1) :
        while idxinfo != [] :
            toMerge = [] # the set of indexes that can be merged with idxstart
            idxstart = idxinfo[0] # pivot index, compares it with all the others
            idxinfo.remove(idxstart) # will cycle through the remaining indexes
            # adds to toMerge all the indexes mergeable with idxstart
            for idxcheck in idxinfo :
                if basicConditions( infosets.iloc[idxstart], infosets.iloc[idxcheck], mergeGroup ) : # conditions to merge
                    if infoloss or samepayoff(infosets['Payoff'][idxstart], infosets['Payoff'][idxcheck]):
                        toMerge.append(idxcheck)
            for tm in toMerge :
                idxinfo.remove(tm) # removes the mergeGroup from the list of indexes
            toMerge.append(idxstart)
            if not infoloss :
                mergeGroup.append(toMerge) # updates
                mergeGroupPay.append(infosets['Payoff'][toMerge[0]])
            else : # proper clustering with information loss
                clustGroup, clustPayh = kmeanscall(toMerge,infosets,sizeofabstraction)
                for cgi in range(len(clustGroup)) :
                    cg = clustGroup[cgi]
                    cp = clustPayh[cgi]
                    if cg != [] :
                        mergeGroup.append(cg)
                        mergeGroupPay.append(cp)
        return mergeGroup, mergeGroupPay

    # The groups that are to be merged are saved in mergeGroup
    for depth in range(1,max(infosets['Depth']) + 1):
        mergeGroup, mergeGroupPay = updateMergeGroup(list(infosets.index[infosets['Depth'] == depth]), mergeGroup, mergeGroupPay, sizeofabstraction = sizeofabstraction)

    # Then we get a new dataframe of merged infosets
    return mergeInfosets(infosets,mergeGroup,mergeGroupPay)

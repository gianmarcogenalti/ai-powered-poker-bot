import pandas as pd
import numpy as np
import time
import re
import math
from sklearn.cluster import KMeans
from conditions import *

# Merges the infosets according to the specified mergeGroup
def mergeInfosets(infosets,mergeGroup,mergeGroupPay) :
    newinfosets = pd.DataFrame()
    
    #preallocates
    pdkeys = ['MapPh1','Map','History_Structure','Depth','Payoff','Player','Actions','Probability','Real_Parents','Real_Sons']
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
        theseSons = []
        for imgi in mergeGroup[img] :
            thisSon = infosets['MapPh1'][infosets['Real_Sons'][imgi]]
            for ts in thisSon :
                if not ts in theseSons :
                    theseSons.append(ts)
        nodoublesSons = theseSons
        newinfosets['Real_Sons'][img] = nodoublesSons
        for s in nodoublesSons :
            newinfosets['Real_Parents'][s].append(img)
        
    return newinfosets

# Calls kmeans algorithm
def kmeanscall(toMerge,infosets) :
    k = round(math.sqrt(len(toMerge))) # k in kmeans
    pv = list()
    [pv.append(infosets['Payoff'][mg]) for mg in toMerge]
    mg = np.array(pv)
    kmeans = KMeans(n_clusters=k, random_state=0).fit(mg)
    labs = kmeans.labels_
    pay = kmeans.cluster_centers_
    clustGroup = list()
    clustPay = pay.tolist()
    [clustGroup.append(list()) for i in range(0,k)]
    ikml = 0
    for kml in labs :
        if toMerge[ikml] != [] :
            clustGroup[kml].append(toMerge[ikml])
        ikml += 1
    return clustGroup, clustPay

# Merges infosets into clusters
def cluster(infosets, infoloss) :
    
    # List of lists: inner lists are to be merged together
    mergeGroup = []
    mergeGroupPay = []
    
    # Updates the mergeGroup with the indexes at idxinfo (at same depth)
    def updateMergeGroup(idxinfo,mergeGroup,mergeGroupPay) :
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
                clustGroup, clustPayh = kmeanscall(toMerge,infosets)
                [mergeGroup.append(cg) for cg in clustGroup if cg != []]
                [mergeGroupPay.append(cg) for cg in range(len(clustPayh)) if clustGroup[cg] != []]
        return mergeGroup, mergeGroupPay
    
    # The groups that are to be merged are saved in mergeGroup
    for depth in range(1,max(infosets['Depth']) + 1):
        mergeGroup, mergeGroupPay = updateMergeGroup(list(infosets.index[infosets['Depth'] == depth]), mergeGroup,mergeGroupPay)
    
    # Then we get a new dataframe of merged infosets
    return mergeInfosets(infosets,mergeGroup,mergeGroupPay)
    
import pandas as pd
import numpy as np
import time
import re

# Are those payoffs the same?
def samepayoff(payoff1,payoff2) :
    l1 = len(payoff1)
    if l1 != len(payoff2):
        return 0
    for ipl in range(0,l1):
        if payoff1[ipl] != payoff2[ipl]:
            return 0
    return 1

# Are the parent MGs the same?
def sameParentsMG(parents1,parents2,mergeGroup) :
    def getparlistinmg(parents,mergeGroup):
        plist = []
        for mgi in range(len(mergeGroup)) :
            for p1 in parents :
                if p1 in mergeGroup[mgi] and not mgi in plist:
                    plist.append(mgi)
        return plist
    return getparlistinmg(parents1,mergeGroup) == getparlistinmg(parents2,mergeGroup)

# Given an infosets dataframe and indexes of two infosets returns 1 if they are
# mergeable (it would be possible to merge them) and 0 otherwise
def basicConditions(infoset1,infoset2,mergeGroup) : # for speed doesn't load all the infoset, just the selected rows
    
    # CHECKS SAME Player, Parents, Structure (Depth already checked)
    
    if(infoset1['Player'] != infoset2['Player']) : # Same Player
        return 0
    
    if(infoset1['Actions'] != infoset2['Actions']) : # Same Actions
        return 0
    
    if infoset1['Real_Parents'] != infoset2['Real_Parents'] : # Same parents
        if not sameParentsMG(infoset1['Real_Parents'],infoset2['Real_Parents'],mergeGroup) : # Parents in same mergeGroup 
            return 0
    
    if(len(infoset1['Payoff']) != len(infoset2['Payoff'])) : # Same payoff length
        return 0
    
    if(infoset1['Depth'] > 1) : # at the 1st level there is no history
        if( infoset1['History_Structure'] != infoset2['History_Structure']) : # Same history
            return 0
    
    return 1
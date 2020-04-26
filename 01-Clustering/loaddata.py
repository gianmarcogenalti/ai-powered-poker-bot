import pandas as pd
import numpy as np
import time
import re

folderpath = "..\\Import-files\\"

# Converts string of array data ("[1.0, 2.0, 3.0]") to the specified array format
def makeArray(text,targetType):
    ret = []
    for t in text :
        if t != '[]' and t != '-1' :
            regex = "(?<=\[)(.*)(?=\])"
            if targetType == "string" :
                regex = "(?<=\[')(.*)(?='\])"
            textwb = re.findall(regex,t)[0]
            if targetType == "string" :
                ret.append(textwb.split("', '"))
            elif targetType == "float" :
                ret.append(list(map(float, np.array(textwb.split(", "))))) 
            elif targetType == "int" :
                ret.append(list(map(int, np.array(textwb.split(", "))))) 
        else :
            ret.append([])
    return ret

# Checks if two histories are the same
def samepath(path1, path2): 
    test = False
    match1 = re.search("(?<=((\?./)|(.\?/)))(.*)", path1)
    match2 = re.search("(?<=((\?./)|(.\?/)))(.*)", path2)
    try:
        k1 = list(match1.group(0))
    except:
        test = True
    try:
        k2 = list(match2.group(0))
    except:
        if test:
            return 1
        else:
            return 0
    if test:
        return 0
    while("C" in k1):
            id = k1.index("C")
            k1[id] = 'alò'
            k1[id+2] = 'alò'
    while("C" in k2):
            id = k2.index("C")
            k2[id] =  'alò'
            k2[id+2] = 'alò'
    return k1 == k2

# Creates an int flag to group structures with
def createstringflag(hist):
    res = []
    flagn = 0
    flagpath = []
    
    for ih in range(0,len(hist)):
        alfl = False
        flagsize = len(flagpath)
        for ifl in range(0,flagsize):
            if samepath(flagpath[ifl],hist[ih]) :
                res.append(ifl)
                alfl = True
                break
        if not alfl :
            flagpath.append(hist[ih])
            res.append(flagsize)
    
    return res

# Returns immediate real parents and sons of the infosets
def realFamily(dads,players) :
    infocount = len(dads)
    resSons = [[] for i in range(infocount)] # Real_Sons (same player)
    resPar = [[] for i in range(infocount)] # Real_Parents (same player)
    sons = [[] for i in range(infocount)] # Sons (other player)
    for ii in range(infocount) :
        dad = dads[ii]
        for d in dad :
            sons[d].append(ii)
    
    def recursiveRealSons(idxdad,player) :
        for s in sons[idxdad] :
            if players[s] == player:
                if not s in resSons[idxdad] :
                    resSons[idxdad].append(s)
                if not idxdad in resPar[s] :
                    resPar[s].append(idxdad)
            recursiveRealSons(s,player)
    
    for d in range(infocount) :
        if dads[d] == [] : # start here
            recursiveRealSons(d,players[d])
            for s in sons[d] :
                recursiveRealSons(s,players[s]) # and here
            
    return resSons, resPar

# Loads the csv and returns it as pd.dataframes in the proper format
def loadinfosets(game): 
    global folderpath

    # Defines the data structure of the csv from parsing
    datastructure = {'History':str,
                     'Members':str,
                     'Depth':int,
                     'Index_Members':str,
                     'Dad':str,
                     'Player':int,
                     'Sons':str,
                     'All_Sons':str,
                     'Parents':str,
                     'Actions':str,
                     'Payoff_Vector_P1':str,
                     'Probability':float}
    
    # Loads the dataframes 
    rawinfosets = pd.read_csv(folderpath + game + "_infosets.csv", dtype = datastructure)
    
    # Builds the real df of infosets
    infosets = pd.DataFrame()
    infosets['History_Structure'] = createstringflag(rawinfosets['History'])
    infosets['Depth'] = rawinfosets['Depth'] 
    infosets['Payoff'] = makeArray(rawinfosets['Payoff_Vector_P1'],"float")
    infosets['Player'] = rawinfosets['Player'] 
    infosets['Real_Sons'], infosets['Real_Parents'] = realFamily(makeArray(rawinfosets['Dad'],"int"),infosets['Player'])
    infosets['Actions'] = makeArray(rawinfosets['Actions'],"string")
    infosets['Probability'] = rawinfosets['Probability']
    infosets['MapPh1'] = [[] for i in range(len(infosets['History_Structure']))]
    infosets['Map'] = [[] for i in range(len(infosets['History_Structure']))]
    
    return infosets, rawinfosets

import pandas as pd
import numpy as np
import re
import math
from sklearn.cluster import KMeans

def realParents(infosets) :
    res = []
    for ii in range(0,len(infosets)) :
        depthpar = 0
        curpar = []
        for ip in infosets['Parents'][ii] :
            if infosets['Depth'][ip] > depthpar :
                curpar = []
                curpar.append(ip)
            else:
                if infosets['Depth'][ip] == depthpar :
                    curpar.append(ip)
        res.append(curpar)
    return res

def kmeanscall(mergeGroup,infosets) :
    k = round(math.sqrt(len(mergeGroup))) # k in kmeans
    pv = list()
    [pv.append(infosets['Payoff Vector P1'][mg]) for mg in mergeGroup]
    mg = np.array(pv)
    #print(mg)
    kmeans = KMeans(n_clusters=k, random_state=0).fit(mg)
    labs = kmeans.labels_
    pay = kmeans.cluster_centers_
    #print("labs")
    #print(labs)
    #print(kmeans.inertia_)
    #print(kmeans.n_iter_)
    clustGroup = list()
    clustPay = pay.tolist()
    [clustGroup.append(list()) for i in range(0,k)]
    ikml = 0
    for kml in labs :
        if mergeGroup[ikml] != [] :
            clustGroup[kml].append(mergeGroup[ikml])
        ikml += 1
    #print("clustGroup")
    #print(clustGroup)
    #print(clustPay)
    return clustGroup, clustPay


def fastClusterer(infosetsMerger,infosets,indcdepth,rp) :
    clustPay = list()
    while indcdepth != [] :
        index1 = indcdepth[0] # pivot index, compares it with all the others
        mergeGroup = [] # the set of indexes that can be merged with index1
        indcdepth.remove(index1) # will cycle through the remaining indexes
        # adds to mergeGroup all the indexes mergeable with index1
        for index2 in indcdepth :
            if conditions(infosets.iloc[index1], infosets.iloc[index2],infosetsMerger,rp[index1],rp[index2]) : # conditions to merge
                #if similarPayoff(infosets['Payoff Vector P1'][index1], infosets['Payoff Vector P1'][index2]):
                mergeGroup.append(index2)
        for mg in mergeGroup :
            indcdepth.remove(mg) # removes the mergeGroup from the list of indexes
        mergeGroup.append(index1) # adds index1 to the mergeGroup

        #print("mergeGroup")
        #print(mergeGroup)
        #kmeans
        clustGroup, clustPayh = kmeanscall(mergeGroup,infosets)
        [infosetsMerger.append(cg) for cg in clustGroup] # adds the final group to the infosetMerger list
        [clustPay.append(cp) for cp in clustPayh]
        '''
        # PRINTS OUT the distance matrix!
        matdist = list()
        for mg1 in mergeGroup :
            matdistrow = list()
            a = np.array(infosets['Payoff Vector P1'][mg1])
            for mg2 in mergeGroup :
                b = np.array(infosets['Payoff Vector P1'][mg2])
                matdistrow.append(np.linalg.norm(a-b))
            matdist.append(matdistrow)
        y=np.array([np.array(matdisto) for matdisto in matdist])
        print(y)
        '''
    return infosetsMerger, clustPay

# returns a vector res of new row indexes:
# res[i] is the row index of infosetsMerger in which infosets[][i] is saved
def mapinfosets(infosets,infosetsMerger) :
    res = []

    for ii in range(0,len(infosets)) :
        res.append(rowinlistoflist(infosetsMerger,ii))

    return res

def mapinfosetsoriginal(infosets,infosetsMerger) :
    res = []

    for ii in range(0,len(infosetsMerger)) :
        curres = list()
        for im in infosetsMerger[ii] :
            curres += infosets['Map'][im]
        res.append(curres)

    return res


# simplifies history: a flag is assigned to every history and the vector of flags (res) is returned
# res[i] is the flag corresponding to the history of infosets[][i]
def createstructure(hist):
    res = []
    flag = []
    flagpath = []

    for ih in range(0,len(hist)):
        alfl = False
        for ifl in range(0,len(flag)):
            if samepath(flagpath[ifl],hist[ih]) :
                res.append(flag[ifl])
                alfl = True
                break
        if not alfl :
            curfl = len(flag)
            flag.append(curfl)
            flagpath.append(hist[ih])
            res.append(curfl)

    return res

# A column of "['a', 'b', 'c']" becomes a column of lists of strings
def makeArray(text):
    ret = []
    for t in text :
        regex = "(?<=\[')(.*)(?='\])"
        match = re.findall(regex,t)
        textwb = match[0]
        ret.append(textwb.split("', '"))
    return ret

# A column of "[1.0, 2.0, 3.0]" becomes a column of lists of floats
def makeArrayFloat(text):
    ret = []
    for t in text :
        regex = "(?<=\[)(.*)(?=\])"
        match = re.findall(regex,t)
        textwb = match[0]
        textl = np.array(textwb.split(", "))
        ret.append(textl.astype(np.float))
    return ret

# A column of "[1, 2, 3]" becomes a column of lists of ints
def makeArrayInt(text):
    ret = []
    for t in text :
        if t != '[]':
            regex = "(?<=\[)(.*)(?=\])"
            match = re.findall(regex,t)
            textwb = match[0]
            textl = np.array(textwb.split(", "))
            ret.append(list(map(int, textl)))
        else :
            ret.append([])
    return ret

# Loads the csvs and returns them as dataframes in the proper format
def loadcsvs(game):
    folderpath = "..\\Import-files\\"
    
    #Loads the dataframes in 2D (lists are loaded as strings)
    infosets = pd.read_csv(folderpath +"ph1_"+ game + ".csv", dtype={'Map':str,'Depth':int,'Payoff Vector P1':str,'Player':int,'Sons':str,'Parents':str,'Structure':int})
    terminals = pd.read_csv(folderpath + game + "_terminals.csv", dtype={'History':str,'Payoff':str})
    nonterminals = pd.read_csv(folderpath + game + "_nonterminals.csv", dtype={'History':str,'Player':int,'Actions':str})
    chances = pd.read_csv(folderpath + game + "_chances.csv", dtype={'History':str,'Actions':str})

    # Calls the functions and converts the columns elements from strings to lists (properly)
    infosets['Map'] = makeArrayInt(infosets['Map']) # float
    infosets['Payoff Vector P1'] = makeArrayFloat(infosets['Payoff Vector P1']) # float
    infosets['Sons'] = makeArrayInt(infosets['Sons']) # int
    infosets['Parents'] = makeArrayInt(infosets['Parents']) # int
    terminals['Payoff'] = makeArrayFloat(terminals['Payoff']) # float
    nonterminals['Actions'] = makeArray(nonterminals['Actions']) # str
    chances['Actions'] = makeArray(chances['Actions']) # str

    return infosets, terminals, nonterminals, chances

# checks if two histories are the same
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

# checks wether two payoffs are similar
def similarPayoff(payoff1,payoff2) :

    l1 = len(payoff1)
    if l1 != len(payoff2):
        return 0
    for ipl in range(0,l1):
        if payoff1[ipl] != payoff2[ipl]:
            return 0

    return 1

# returns the row indexes of infosets with the specified depth
def inddepth(infosets,depth) :
    ins = list()
    for i1 in range(0,infosets['Depth'].size) :
        if infosets['Depth'][i1] == depth:
            ins.append(i1)
    return ins

# checks if el is an element of an element of listoflist
def isinlistoflist(listoflist,el) :
    for list1 in listoflist :
        try:
            if el in list1:
                return 1
        except:
            if el == list1:
                return 1
    return 0

# finds the row index of the list of which el is an element
def rowinlistoflist(listoflist,el) :
    il = 0
    for list1 in listoflist :
        try:
            if el in list1:
                return il
        except:
            if el == list1:
                return il
        il += 1
    return -1

def sameParentsinIM(infosetsMerger,rp1,rp2) :
    for rp1i in rp1 :
        if isinlistoflist(infosetsMerger,rp1i) :
            row = rowinlistoflist(infosetsMerger,rp1i)
            for rp2i in rp2 :
                if not (rp2i in infosetsMerger[row]) :
                    return 0
            return 1
    return 0

# given an infosets dataframe and indexes of two infosets returns 1 if they are
# mergeable (it would be possible to merge them) and 0 otherwise
def conditions(infoset1, infoset2,infosetsMerger,rp1,rp2) : # for speed doesn't load all the infoset, just the selected rows

    # CHECKS SAME Player, Parents, Structure (Depth already checked in main)

    if(infoset1['Player'] != infoset2['Player']) : # Same player
        #print("Different Players!")
        return 0

    if(infoset1['Parents'] != infoset2['Parents']) : # Same parents
        if not sameParentsinIM(infosetsMerger,rp1,rp2) : # Same parents
            return 0

    if(len(infoset1['Payoff Vector P1']) != len(infoset2['Payoff Vector P1'])) : # Same player
        #print("Different Players!")
        return 0

    if(infoset1['Depth'] > 1) : # at the 1st level there is no history
        if( infoset1['Structure'] != infoset2['Structure']) : # Same history
            #print("Different Structures!")
            return 0

    return 1

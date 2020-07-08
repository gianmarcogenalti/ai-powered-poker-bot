import numpy as np
import re

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

def init_probabilities(infosets):
    probabilities = [[] for _ in range(len(infosets.index))]
    regrets = [[] for _ in range(len(infosets.index))]
    for index,row in infosets.iterrows():
        n_actions = len(row.Actions)
        regrets[index] = list(np.zeros(n_actions))
        for pr_act in range(n_actions):
            probabilities[index].append(1/n_actions)
    infosets['Actions_Prob'] = probabilities
    return probabilities, regrets

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

def mult_intersection(lst1, lst2):
    lst3 = [list(filter(lambda x: x in lst1, sublist)) for sublist in lst2]
    return lst3

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def chance_to_infoset(nodes, abs_infosets):
    chances = nodes[nodes.Type == 'C']
    nmax = len(abs_infosets.index)
    counter = 0
    for index,crow in chances.iterrows():
        nodes.Abs_Map[index] = nmax + counter
        counter += 1
        cdf = pd.DataFrame([index], columns = ['Map'])
        abs_infosets = abs_infosets.append(cdf, ignore_index=True)

    return abs_infosets

import re
import pandas as pd
import numpy as np


def abstractnodes(nodes, abs_infosets, infosets):
    newpo1  = [[] for _ in range(len(nodes.index))]
    abmap   = [[] for _ in range(len(nodes.index))]
    members = [[] for _ in range(len(abs_infosets.index))]
    prob_opp = np.ones(len(nodes.index))
    exp_U   = np.zeros(len(nodes.index))

    for abindex, abrow in abs_infosets.iterrows():
        for m in abrow.Map:
            members[abindex] = members[abindex] + infosets.Index_Members[m]
        for i in infosets.Index_Members[m]:
            sz = len(nodes.Payoff_Vector_P1[i])
            newpo1[i] = abrow.Payoff[:sz]
            abmap[i]  = abindex
            counter = 0
            for ds in nodes.Direct_Sons[i]:
                if nodes.Type[ds] == 'L':
                    newpo1[ds] = newpo1[i][counter]
                counter += 1
                #
            #
        #
    #

    nodes['Probability_Opp']      = prob_opp
    #nodes['Payoff_Vector_P1']     = newpo1
    #nodes['Abstract_Map']         = abmap
    abs_infosets['Index_Members'] = members
    nodes['Exp_Utility']          = exp_U

def maptoclust(infosets,abs_infosets):
    map = [[] for _ in range(len(infosets))]
    for index,row in abs_infosets.iterrows():
        for inf in row.Map:
            map[inf] = index
        #
    #
    infosets['Map_Clust'] = map

def abstractsons(nodes, abs_infosets, infosets):
    direct_sons = []
    prob_sons   = []
    abs_payoff  = []
    for index, row in abs_infosets.iterrows():
        temp_son = [[] for _ in range(len(row.Actions))]
        temp_prob = [[] for _ in range(len(row.Actions))]
        temp_payoff = [[] for _ in range(len(row.Actions))]
        for m in row.Index_Members:
            counter = 0
            prob_m = nodes.Nature_Prob[m]
            for ds in nodes.Direct_Sons[m]:
                if nodes.Type[ds] != 'C' and nodes.Type[ds] != 'L':
                    if infosets.Map_Clust[nodes.Map[ds]] not in temp_son[counter]:
                        temp_son[counter].append(infosets.Map_Clust[nodes.Map[ds]])
                        temp_prob[counter].append(prob_m)
                    else:
                        fnd = temp_son[counter].index(infosets.Map_Clust[nodes.Map[ds]])
                        temp_prob[counter][fnd] += prob_m

                if nodes.Type[ds] == 'C':
                    counter2 = 0
                    for ns in nodes.Direct_Sons[ds]:
                        nat_probs = nodes.Actions_Prob[ds]
                        if infosets.Map_Clust[nodes.Map[ns]] not in temp_son[counter]:
                            temp_prob[counter].append(prob_m * nat_probs[counter2])
                            temp_son[counter].append(infosets.Map_Clust[nodes.Map[ns]])
                        else:
                            fnd = temp_son[counter].index(infosets.Map_Clust[nodes.Map[ns]])
                            temp_prob[counter][fnd] += prob_m * nat_probs[counter2]
                        counter2 += 1
                if nodes.Type[ds] == 'L':
                    temp_payoff[counter].append(nodes.Payoff_Vector_P1[ds][0])
                    temp_prob[counter].append(prob_m)
                counter+= 1

        counter3 = 0
        for list in temp_prob:
            sm = sum(list)
            temp = []
            for i in list:
                temp.append(i/sm)
            temp_prob[counter3] = temp
            counter3 += 1
        res = []

        single_payoff = []
        counter4 = 0
        for list in temp_payoff:
            if len(list) != 0:
                wm = 0
                for i in range(len(list)):
                    wm += list[i]*temp_prob[counter4][i]
                single_payoff.append(wm)
            else:
                single_payoff.append(-1000)
            counter4+=1


        prob_sons.append(temp_prob)
        direct_sons.append(temp_son)
        abs_payoff.append(single_payoff)

    abs_infosets['Direct_Sons']   = direct_sons
    abs_infosets['Nature_Weight'] = prob_sons
    abs_infosets['Payoff_P1']     = abs_payoff

def abstractdads(abs_infosets):
    dads = [[] for _ in range(len(abs_infosets.index))]
    for abindex,row in abs_infosets.iterrows():
        for action in row.Direct_Sons:
            for ds in action:
                if abindex not in dads[ds]:
                    dads[ds].append(abindex)
            #
        #
    #
    abs_infosets['Dads'] = dads


def update_natureprob(nodes):
    nodes['Nature_Prob'] = [1.00] * len(nodes.index)
    for dpt in range(max(nodes.Depth)+1):
        for index,row in nodes[nodes.Depth == dpt].iterrows():
            if row.Direct_Sons != -1:
                counter = 0
                for ds in row.Direct_Sons:
                    if nodes.Type[index] == 'C':
                        nodes.Nature_Prob[ds] = nodes.Nature_Prob[index] * row.Actions_Prob[counter]
                    else:
                        nodes.Nature_Prob[ds] = nodes.Nature_Prob[index]
                    counter = counter + 1
                #
            #
        #
    #
    nodes['Probability'] = nodes['Nature_Prob']
def get_back(infosets, abs_infosets, strategies):
    probos = []
    for i in abs_infosets.index:
        probos.append(strategies[i])
    abs_infosets['Actions_Prob'] = probos
    act_probs = []
    for index,row in infosets.iterrows():
        act_probs.append(strategies[row.Map_Clust])
    infosets['Actions_Prob'] = act_probs

def abs_depth(abs_infosets):
    depths = []
    for index,row in abs_infosets.iterrows():
        np = row.History.count("P")
        #nc = row.History.count("C")
        depths.append(np  + 1)

    abs_infosets['Depth'] = depths


def nodeblueprint(nodes, abs_infosets):
    #actprobs = [[] for _ in range(len(nodes.index))]
    for index,row in nodes.iterrows():
        if row.Type == 'N':
            nodes.Actions_Prob[index] = abs_infosets.Actions_Prob[row.Abs_Map]
    #nodes['Actions_Prob'] = actprobs

def absnature(nodes, infosets, abs_infosets):
    nature_w = [[] for _ in range(len(abs_infosets.index))]
    for index, row in abs_infosets.iterrows():
        sm = 0
        print(row)
        for member in row.Index_Members:
            sm += nodes.Nature_Prob[member]
        for member in row.Index_Members:
            nature_w[index].append(nodes.Nature_Prob[member]/sm)

    abs_infosets['Nature_Prob'] = nature_w

def nodetoclust(nodes, infosets, abs_infosets):
    map = []
    for index, row in nodes.iterrows():
        if row.Type == 'N':
            maptoinf = row.Map
            maptoclust = infosets.Map_Clust[maptoinf]
            #print(maptoinf, maptoclust)
        else:
            maptoclust = -999999
        #print(maptoclust)
        map.append(maptoclust)

    nodes['Abs_Map'] = map

def chance_to_infoset(nodes, abs_infosets):
    chances = nodes[nodes.Type == 'C']
    nmax = len(abs_infosets.index)
    counter = 0
    for index,crow in chances.iterrows():
        nodes.Abs_Map[index] = nmax + counter
        counter += 1
        cdf = pd.DataFrame([index], columns = ['Map'])
        cdf['Dads'] = 999999
        abs_infosets = abs_infosets.append(cdf, ignore_index=True)

    return abs_infosets

def update_infoprob(infosets, nodes):
    prob = [0] * len(infosets.index)
    for index, row in infosets.iterrows():
        for map in row.Index_Members:
            prob[index] = prob[index] + nodes.Probability[map]
        #
    #
    infosets['Probability'] = prob

def prob_leaf(nodes) :
    sum = 0
    for index,row in nodes.iterrows():
        if row.Type == 'L':
            sum = sum + row.Probability
        #
    #
    print('Leaves sum to: ', sum)

def update_nodeprob(nodes):
    expos = [0 for i in range(len(nodes))]
    probos = [0 for i in range(len(nodes))]
    def recursivethings(icn):
        if nodes.Direct_Sons[icn] != -1:
            for ids,ds in enumerate(nodes.Direct_Sons[icn]):
                ds = nodes.Direct_Sons[icn][ids]
                try:
                    ap = nodes.Actions_Prob[icn][ids]
                except:
                    ap = nodes.Actions_Prob[icn][nodes.Actions[icn][ids]]
                probos[ds] = ap * probos[icn]
                expos[icn] += ap * recursivethings(ds)
        else:
            expos[icn] = nodes.Payoff_P1[icn]
        return expos[icn]

    start = nodes.index[-1]
    probos[start] = 1
    recursivethings(start)
    nodes['Expected_Payoff'] = expos
    nodes['Probability'] = probos

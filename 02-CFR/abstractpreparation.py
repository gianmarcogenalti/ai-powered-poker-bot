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
    nodes['Abstract_Map']         = abmap
    abs_infosets['Index_Members'] = members
    nodes['Exp_Utility']          = exp_U

def maptoclust(infosets,abs_infosets):
    map = [[] for _ in range(len(infosets.index))]
    for index,row in abs_infosets.iterrows():
        for inf in row.Map:
            map[inf].append(index)
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
                    if infosets.Map_Clust[nodes.Map[ds]][0] not in temp_son[counter]:
                        temp_son[counter].append(infosets.Map_Clust[nodes.Map[ds]][0])
                        temp_prob[counter].append(prob_m)
                    else:
                        fnd = temp_son[counter].index(infosets.Map_Clust[nodes.Map[ds]][0])
                        temp_prob[counter][fnd] += prob_m

                if nodes.Type[ds] == 'C':
                    counter2 = 0
                    for ns in nodes.Direct_Sons[ds]:
                        nat_probs = nodes.Actions_Prob[ds]
                        if infosets.Map_Clust[nodes.Map[ns]][0] not in temp_son[counter]:
                            temp_prob[counter].append(prob_m * nat_probs[counter2])
                            temp_son[counter].append(infosets.Map_Clust[nodes.Map[ns]][0])
                        else:
                            fnd = temp_son[counter].index(infosets.Map_Clust[nodes.Map[ns]][0])
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


def update_nodeprob(nodes):
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

import re
import pandas as pd
import numpy as np
'''
def histoparents(infosets):
    opparents  = [[] for _ in range(len(infosets.index))]
    oppactions = [[] for _ in range(len(infosets.index))]
    for index, row in infosets.iterrows():
        hist = row.History[4:]
        regexchance = 'C:'
        regex = '(?<=\:)(.){1,6}$'
        ix = hist.find(regexchance)
        if ix != -1:
            hist = hist[:ix] + hist[ix+4:]
        if row.Player == 1:
            opponent = 2
        else:
            opponent = 1
        for pindex, prow in infosets[infosets.Depth < row.Depth].iterrows():
            phist = prow.History[4:]
            pix = phist.find(regexchance)
            if pix != -1:
                phist = phist[:ix] + phist[ix+4:]
            if phist in hist and prow.Player == opponent and phist != "" and hist != "":
                opparents[index].append(pindex)
                match = re.search(regex, phist)
                oppactions[index].append(match[0])

    infosets['Opponent_Parents'] = opparents
    infosets['Opponent_Actions'] = oppactions

'''


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
    nodes['Payoff_Vector_P1']     = newpo1
    nodes['Abstract_Map']         = abmap
    abs_infosets['Index_Members'] = members
    nodes['Exp_Utility']          = exp_U

def abstractsons(nodes, abs_infosets):
    direct_sons = []
    prob_sons   = []
    for index, row in abs_infosets.iterrows():
        temp_son = [[] for _ in range(len(row.Actions))]
        temp_prob = [[] for _ in range(len(row.Actions))]
        for m in row.Index_Members:
            counter = 0
            prob_m = nodes.Nature_Prob[m]
            for ds in nodes.Direct_Sons[m]:
                if nodes.Type[ds] != 'C':
                    temp_son[counter].append(ds)
                    temp_prob[counter].append(prob_m)
                else:
                    counter2 = 0
                    for ns in nodes.Direct_Sons[ds]:
                        nat_probs = nodes.Actions_Prob[ds]
                        temp_prob[counter].append(prob_m * nat_probs[counter2])
                        temp_son[counter].append(ns)
                        counter2 += 1
                counter += 1
        direct_sons.append(temp_son)

        counter = 0
        for list in temp_prob:
            sm = sum(list)
            temp = []
            for i in list:
                temp.append(i/sm)
            temp_prob[counter] = temp
            counter += 1

        prob_sons.append(temp_prob)

    abs_infosets['Direct_Sons']   = direct_sons
    abs_infosets['Nature_Weight'] = prob_sons

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

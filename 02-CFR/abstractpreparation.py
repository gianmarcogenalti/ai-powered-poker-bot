import re
import pandas as pd

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


def abstractnodes(nodes, abs_infosets, infosets):
    newpo1  = [[] for _ in range(len(nodes.index))]
    abmap   = [[] for _ in range(len(nodes.index))]
    members = [[] for _ in range(len(abs_infosets.index))]

    for abindex, abrow in abs_infosets.iterrows():
        for m in abrow.Map:
            members[abindex] = members[abindex] + infosets.Index_Members[m]
            for i in infosets.Index_Members[m]:
                sz = len(nodes.Payoff_Vector_P1[i])
                newpo1[i] = abrow.Payoff[:sz]
                abmap[i]  = abindex

    nodes['Payoff_Vector_P1']     = newpo1
    nodes['Abstract_Map']         = abmap
    abs_infosets['Index_Members'] = members

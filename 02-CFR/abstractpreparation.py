import re
import pandas as pd

infosets = pd.read_csv("..\\Import-Files\\leduc3_infosets.csv")

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
            if prow.History in row.History and prow.Player == opponent:
                opparents[index].append(pindex)
                match = re.search(regex, prow.History)
                oppactions[index].append(match[0])


    infosets['Opponent_Parents'] = opparents
    infosets['Opponent_Actions'] = oppactions

histoparents(infosets)
print(infosets.Opponent_Parents)

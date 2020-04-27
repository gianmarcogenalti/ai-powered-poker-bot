
import pandas as pd
from loaddata import *

def probabilities_update() :
    nodes = pd.read_csv("..\\Import-files\\leduc5_nodes.csv")
    nodescount = len(nodes['Actions'])
    for ii in range(nodescount) :
        if nodes.Direct_Sons[ii] == "-1" :
            nodes.Direct_Sons[ii] = "[]"
        if nodes.Actions_Prob[ii] == "END" :
            nodes.Actions_Prob[ii] = "[]"
    nodes.Direct_Sons = makeArray(nodes.Direct_Sons,"int")
    nodes.Actions_Prob = makeArray(nodes.Actions_Prob,"float")
    startingnodeidx = nodes.index[nodes.Depth == 0][0]
    
    def recursive_probs(idxcurnode) :
        if nodes.Direct_Sons[idxcurnode] != -1 :
            for idson in range(len(nodes.Direct_Sons[idxcurnode])) :
                dson = nodes.Direct_Sons[idxcurnode][idson]
                nodes.Probability[dson] = nodes.Probability[idxcurnode] * nodes.Actions_Prob[idxcurnode][idson]
                recursive_probs(dson)
    
    nodes['Probability'][startingnodeidx] = 1
    recursive_probs(startingnodeidx)
    
probabilities_update()
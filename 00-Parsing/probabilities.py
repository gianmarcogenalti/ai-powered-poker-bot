def standardchance(chances):
    stdprob = [[] for _ in range(len(chances.index))]
    for index, row in chances.iterrows():
        totodd = sum(row.Odds)
        for odd in row.Odds[0:len(row.Odds)-1]:
            stdprob[index].append(odd/totodd)
            #
        stdprob[index].append(1-sum(stdprob[index]))
    #
    chances['Probabilities'] = stdprob

def nodeprob(nodes, chances):
    prob = [1] * len(nodes.index)
    nodes['Probabilities'] = prob
    for cindex, crow in chances.iterrows():
        counter = 0
        for move in crow.Actions:
            if crow.History != '/':
                son = crow.History + '/C:' + move
            else:
                son = crow.History + 'C:' + move
            i = nodes.index.values[nodes.History == son]
            nodes.Probabilities[i] = nodes.Probabilities[i]*crow.Probabilities[counter]
            for sons in nodes.Sons[i]:
                nodes.Probabilities[sons] = nodes.Probabilities[sons] * crow.Probabilities[counter]
            #
            counter = counter + 1
        #
    #

def uniform_actionprob(infosets,nodes):
    uniprobi = [[] for _ in range(len(infosets.index))]
    uniprobn = [[] for _ in range(len(nodes.index))]
    for index, row in infosets.iterrows():
        uni = 1/len(row.Actions)
        uniprobi[index] = [uni] * len(row.Actions)
        #
    #
    for index, row in nodes.iterrows():
        uni = 1/len(row.Actions)
        uniprobn[index] = [uni] * len(row.Actions)
        #
    #
    infosets['Actions_Prob'] = uniprobi
    nodes['Actions_Prob'] = uniprobn

def update_nodeprob(nodes):
    prob = [0] * len(nodes.index)
    for index,row in nodes.iterrows():

        direct_sons = []
        moves = []

        if row.Player == 1:
            str = '/P1:'
        else:
            str = '/P2:'

        for move in row.Actions:
            moves.append(row.History + str + move + '/C:')

        for son in row.Sons:
            if (nodes.Depth[son] - row.Depth == 1) or (nodes.Depth[son] - row.Depth == 2 and nodes.History[son][:-1] in moves):
                direct_sons.append(son)
            #
        #
        for son in direct_sons:
            counter = 0
            for move in row.Actions:
                if (row.History + str + move) == nodes.History[son] or (row.History + str + move + '/C:') == nodes.History[son][:-1]:
                    nodes.Probabilities[son] = nodes.Probabilities[son] * row.Actions_Prob[counter]
                #
                counter = counter + 1
            #
        #
    #

## THIS WORKS USING NONTERMINAL NODES
def update_infoprob(infosets, nodes):
    prob = [0] * len(infosets.index)
    for index, row in infosets.iterrows():
        for map in row.Index_Members:
            prob[index] = prob[index] + nodes.Probabilities[map]
        #
    #
    infosets['Probabilities'] = prob

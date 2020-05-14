def update_nodeprob(nodes):
    nodes['Probability'] = [1.00] * len(nodes.index)
    for dpt in range(max(nodes.Depth)+1):
        for index,row in nodes[nodes.Depth == dpt].iterrows():
            if row.Direct_Sons != -1:
                counter = 0
                for ds in row.Direct_Sons:
                    if nodes.Player[index] == 0:
                        nodes.Probability[ds] = nodes.Probability[index] * row.Actions_Prob[counter]
                    else:
                        nodes.Probability[ds] = nodes.Probability[index]
                    counter = counter + 1
                #
            #
        #
    #


## THIS WORKS USING NONTERMINAL NODES
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

def update_nodeprob(nodes):
    nodes['Probability'] = [1.00] * len(nodes.index)
    for dpt in range(0, max(nodes.Depth)):
        for index,row in nodes.iterrows():
            if row.Depth == dpt and row.Direct_Sons != -1:
                counter = 0
                for ds in row.Direct_Sons:
                    nodes.Probability[ds] = nodes.Probability[index] * row.Actions_Prob[counter]
                    counter = counter + 1
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
'''##Useless
def prob_check(dataframe):
    for dpt in range(0, max(dataframe['Depth'])):
        depthdf = dataframe[dataframe.Depth == dpt]
        print(depthdf.Probability)
        sum = 0
        for prob in depthdf.Probability:
            sum = sum + prob
        print("Total Probability at depth ", dpt)
        print(" is ", sum)
'''
def prob_leaf(nodes) :
    sum = 0
    for index,row in nodes.iterrows():
        if row.Type == 'L':
            sum = sum + row.Probability
        #
    #
    print('Leaves sum to: ', sum)

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

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

def payoffvectors(infosets,nodes):
    pv1 = []
    terminals = nodes[nodes.Type == 'L']
    #pv2 = [[] for _ in range(len(infosets.index))]
    for index,row in infosets.iterrows():
        for member in row.Members:
            payoff = []
            for tindex,terminal in terminals.iterrows():
                if terminal.History.find(member) != -1:
                    c1 = terminal.Payoff_P1
                    #c2 = -c1
                    payoff.append(c1)
                #
            #
        #
        pv1.append(payoff)
    #
    infosets['Payoff_Vector_P1'] = pv1

def payoffvectors(nodes):
    last = '(?<=\:)(.*)$'
    pv1 = [[[] for _ in range(0,100)] for _ in range(len(nodes.index))]
    for leaf in nodes.iloc[nodes.index[nodes.Type == 'L'].tolist()]:
        def recursivepo(dad):

            if dad.Sons == []:
                for member in dad.Index_Members:



            for idxson in dad.Sons:
                if(infosets.Depth[idxson] == dad.Depth + 1):
                    son = infosets.iloc[idxson]

                    pv1[dad.name][] = pv1[dad.name] + recursivepo(son) + [idxson]

            return pv1[dad.name]

        recursivepo(root)

    infosets['Payoff_Vector_P1'] = pv1
'''

'''
def nodedescendents(nodes) : ##outdated
    descendent = [[] for _ in range(len(nodes.index))]
    for index,row in nodes[nodes.Type == 'L'].iterrows() :
        if(row.History == '/'):
            descendent[index] = nodes.index.values
        else:
            nd = nodes.where(nodes.History.str.find(row.History + '/') != -1)
            nd = nd.dropna()
            descendent[index] = nd.index.values
    #
    nodes['Sons'] = descendent

    def ispayoffs(infosets, nodes):
        ispo1 = [[] for _ in range(len(infosets.index))]
        for index,row in infosets.iterrows():
            for i in row.Index_Members:
                ispo1[index] += nodes.Payoff_Vector_P1[i]
            #
        #
        infosets['Payoff_Vector_P1'] = ispo1
'''

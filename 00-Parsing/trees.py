from anytree import AnyNode, RenderTree
import pandas as pd
import re

nodes = pd.read_csv("..\\Import-Files\\leduc3_nodes.csv")

def nodestree(nodes):
    root = AnyNode(name = 'C')
    tree = [[] for _ in range(len(nodes.index))]
    last = '(?<=/)(.*)$'
    before = '()'
    for index,row in nodes[nodes.Depth == 1].iterrows():
        tree[index] = AnyNode(name = (re.search(last, row.History))[0], parent = root)

    print(tree)

    for dpt in range(2,max(nodes.Depth)):
        for index,row in nodes[nodes.Depth == dpt].iterrows():
            if(row.Type != 'L'):
                tree[index] = AnyNode(name = (re.search(last, row.History))[0], parent = tree[row.Dad])
            if(row.Type == 'L'):
                tree[index] = AnyNode(name = (re.search(last, row.History))[0], parent = tree[row.Dad], payoffs = nodes.Payoff_P1[index])

    print(RenderTree(root))



last = '(?<=/)(.*)$'
dad = re.search(last, '/C:JJ/P1:raise2/P2:raise2/P1:c/C:Q/P1:raise4/P2:raise4/P1:c')[0]
print(dad)

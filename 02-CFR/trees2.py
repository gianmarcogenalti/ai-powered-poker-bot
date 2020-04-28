from anytree import AnyNode, RenderTree
import pandas as pd
import re

nodes = pd.read_csv("..\\Import-Files\\leduc3_nodes.csv")
infosets = pd.read_csv("..\\Import-Files\\leduc3_infosets.csv")

def nodestree(nodes, attr = None):
    attribute = "name"
    attribute = attr
    original_sin = nodes[nodes.History == '/']
    root = AnyNode(name = 'C', actions = original_sin.Actions)
    tree = [[] for _ in range(len(nodes.index))]
    for index,row in nodes[nodes.Depth == 1].iterrows():
        tree[index] = AnyNode(name = row.History.split('/')[-1],
                              parent = root,
                              payoffs = nodes.Payoff_Vector_P1[index],
                              actions = nodes.Actions[index],
                              probability = nodes.Probability[index],
                              prob_opp = nodes.Probability_Opp[index])

    for dpt in range(2,max(nodes.Depth)):
        for index,row in nodes[nodes.Depth == dpt].iterrows():
            if nodes.Type[index] != 'C':
                tree[index] = AnyNode(name = row.History.split('/')[-1],
                                      parent = tree[row.Dad],
                                      payoffs = nodes.Payoff_Vector_P1[index],
                                      actions = nodes.Actions[index],
                                      probability = nodes.Probability[index],
                                      prob_opp = nodes.Probability_Opp[index])
            else:
                tree[index] = AnyNode(name = row.History.split('/')[-1],
                                      parent = tree[row.Dad],
                                      payoffs = 'Chance',
                                      actions = nodes.Actions[index],
                                      probability = nodes.Probability[index],
                                      prob_opp = nodes.Probability_Opp[index])

    print(RenderTree(root).by_attr(attribute))

def istree(infosets):
    root = AnyNode(name = 'C')
    tree = [[] for _ in range(len(infosets.index))]
    for rindex,row in infosets[infosets.Depth == 1].iterrows():
        tree[rindex] = AnyNode(name = row.History.split('/')[-1], parent = root)

    for dpt in range(2,max(infosets.Depth)):
        for index,row in infosets[infosets.Depth == dpt].iterrows():
            tree[index] = AnyNode(name = row.History.split('/')[-1], parent = tree[row.Dad[0]], payoffs = nodes.Payoff_Vector_P1[index])


    print(RenderTree(tree[45]).by_attr('payoffs'))

#nodestree(nodes)

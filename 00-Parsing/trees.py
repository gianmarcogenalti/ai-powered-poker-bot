from anytree import AnyNode, RenderTree
import pandas as pd
import re

nodes = pd.read_csv("..\\Import-Files\\leduc3_nodes.csv")
infosets = pd.read_csv("..\\Import-Files\\leduc3_infosets.csv")

def nodestree(nodes):
    root = AnyNode(name = 'C')
    tree = [[] for _ in range(len(nodes.index))]
    for index,row in nodes[nodes.Depth == 1].iterrows():
        tree[index] = AnyNode(name = row.History.split('/')[-1], parent = root, payoffs = nodes.Payoff_Vector_P1[index])

    for dpt in range(2,max(nodes.Depth)):
        for index,row in nodes[nodes.Depth == dpt].iterrows():
            tree[index] = AnyNode(name = row.History.split('/')[-1], parent = tree[row.Dad], payoffs = nodes.Payoff_Vector_P1[index])


    print(RenderTree(root).by_attr('payoffs'))

def istree(infosets):
    tree = [[] for _ in range(len(infosets.index))]
    for rindex,row in infosets[infosets.Depth == 1].iterrows():
        tree[rindex] = AnyNode(name = row.History.split('/')[-1], payoffs = infosets.Payoff_Vector_P1[rindex])

        for dpt in range(2,max(nodes.Depth)):
            for index,row in infosets[infosets.Depth == dpt].iterrows():
                if(row.Dad != -1):
                    tree[index] = AnyNode(name = row.History.split('/')[-1], parent = tree[row.Dad], payoffs = nodes.Payoff_Vector_P1[index])

        print(RenderTree(tree[rindex]).by_attr('payoffs'))

istree(infosets)
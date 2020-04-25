import time
import pandas as pd
from dataframeparsing import *
from df_reinforcement import *
from probabilities import *

t0 = time.time()

## Available games

kuhn = 'input - kuhn.txt'
l3 = 'input - leduc3.txt'
l5 = 'input - leduc5.txt'

game = l5 # Game to play
game_for_csv = "leduc5" # name to use on the .csv file
print('Chosen game: ', game_for_csv, '\n')
## Path to store the .csv files and names of the ifles

path = '..\\Import-files'
infopath = path + '\\' + game_for_csv + '_infosets.csv'
nodespath = path + '\\' + game_for_csv + '_nodes.csv'

## Creating dataframes

infosets = infosetdf(game) ## Infosets dataframe: 'History',
                            # 'Members' (histories of nodes that compose the infoset),
                            # 'Depth' (number of moves to reach the infoset)
print('infosets created!\n')

nodes = nodesdf(game) ## Full nodes dataframe: 'History', 'Type' (typology of the node)

print('nodes created!\n')

## Reinforcing dataframes with additional informations

nodesdepth(nodes)# adding the "parents" of a node: all the nodes from which the node is reachable
print('depth added to nodes!\n')

maptois(nodes, infosets) # adding a map that sends a node to the infoset he belongs using dataframe indices
print('map to infosets added to nodes!\n')

payoffdescendents(nodes, infosets) # adding the "sons" of a node: all the nodes reachable moving forward from the node,
print('sons added to nodes!\n') # also adding the payoff vector of a node
print('payoff vectors added to nodes!\n')
print('payoff vectors added to infosets!\n')

directsons(nodes) # adding vector of "direct sons" of a node
print('direct sons added to nodes!\n')

nodeantenates(nodes) # adding the parents of a node
directparent(nodes, infosets)
print('parents added to nodes!\n')

indexmembers(infosets, nodes) # same of the 'Members' column but using the indices of the 'nodes' dataframe
print('indexed members added to infosets!\n')

isplayers(infosets, nodes) # adding the player that moves in the infoset
print('players added to infosets!\n')

descendents(infosets) # adding the "sons" of an infoset: all the infosets reachable moving forward from the infoset
alldescendents(infosets)
print('sons added to infosets!\n')

antenates(infosets) # adding the "parents" of an infoset: all the infosets from which the infoset is reachable
print('parents added to infosets!\n')

isactions(infosets,nodes) # adding possible actions to an infoset using the map with  nodes
print('actions added to infosets!\n')
'''
payoffvectors(infosets,nodes) # adding all the possible payoffs reachable from the infoset: it adds the vector for P1
print('payoff vectors added to infosets!\n')
'''
update_nodeprob(nodes) # adding probabilities of chance nodes
print('probabilities added to nodes!\n')

update_infoprob(infosets,nodes) # updating infosets' probabilities by sum of nodes' Probabilities
print('infosets probabilities updated!')

prob_leaf(nodes)

print(nodes)

#prob_check(nonterminals)

## Writing dataframes on a tre and on a .csv file
#nodestree = totree(nodes)
infosets.to_csv(infopath, index = False, header = True, escapechar=' ')
nodes.to_csv(nodespath, index = False, header = True, escapechar=' ')

print('Execution time: ', time.time() - t0)

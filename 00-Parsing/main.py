import time
import pandas as pd
from dataframeparsing import *
from df_reinforcement import *
from probabilities import *
import csv

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
nonterminalpath = path + '\\' + game_for_csv + '_nonterminals.csv'
terminalpath = path + '\\' + game_for_csv + '_terminals.csv'
chancepath = path + '\\' + game_for_csv + '_chances.csv'

## Creating dataframes

chances = chancedf(game) ## Chance node dataframe: 'History' (sequence of moves that lead to the node),
                          #'Odds' (possible draws from the deck with their odds)
print('chances created!\n')

infosets = infosetdf(game) ## Infosets dataframe: 'History',
                            # 'Members' (histories of nodes that compose the infoset),
                            # 'Depth' (number of moves to reach the infoset)
print('infosets created!\n')

terminals = terminaldf(game) ## Terminals nodes (leaves) dataframe: 'History',
                              # 'Payoff' (payoffs of the leaf :[P1 payoff, P2 payoff])
print('terminals created!\n')

nonterminals = nonterminaldf(game) ## Non-Terminal nodes dataframe: 'History',
                                    # 'Player' (player that moves),
                                    # 'Actions' (possible actions he can do)
print('nonterminals created!\n')

## Reinforcing dataframes: adding columns with additional informations

payoffvectors(infosets,terminals) # adding all the possible payoffs reachable from the infoset: two columns, one for P1 and one for P2
print('payoff vectors added to infosets!\n')

isplayers(infosets, nonterminals) # adding the player that moves in the infoset
print('players added to infosets!\n')

descendents(infosets) # adding the "sons" of an infoset: all the infosets reachable moving forward from the infoset
alldescendents(infosets)
print('sons added to infosets!\n')

antenates(infosets) # adding the "parents" of an infoset: all the infosets from which the infoset is reachable
print('parents added to infosets!\n')

maptois(nonterminals, infosets) # adding a map that sends a node to the infoset he belongs using dataframe indices
print('map to infosets added to nodes!\n')

nodedepth(nonterminals, infosets) # adding the depth of a node
print('depth added to nodes!\n')

indexmembers(infosets, nonterminals) # same of the 'Members' column but using the indices of the 'nonterminals' dataframe
print('indexed members added to infosets!\n')

isactions(infosets,nonterminals) # adding possible actions to an infoset using the map with nonterminal nodes
print('actions added to infosets!\n')

nodedescendents(nonterminals) # adding the "sons" of a node: all the nodes reachable moving forward from the node
print('sons added to nodes!\n')

nodeantenates(nonterminals) # adding the "parents" of a node: all the nodes from which the node is reachable
print('parents added to nodes!\n')

standardchance(chances) # standardizing probabilities of chance nodes
print('chance nodes probabilities standardized!\n')

nodeprob(nonterminals, chances) # adding initial probabilities to nodes (initialized as RANDOM PLAYERS' CHOICES)
print('probabilities added to nodes!\n')

uniform_actionprob(infosets, nonterminals) # initializing infosets' actions probabilities as uniform
print('action probabilities initialized as uniform in infosets and nodes!\n')

update_nodeprob(nonterminals) # initializing probabilities of reaching a given infoset
print('nodes probabilities updated!')

update_infoprob(infosets,nonterminals) # updating infosets' probabilities by sum of nodes' Probabilities
print('infosets probabilities updated!')

## Writing dataframes on a .csv file

infosets.to_csv(infopath, index = False, header = True, escapechar=' ')
nonterminals.to_csv(nonterminalpath, index = False, header = True, escapechar=' ')
terminals.to_csv(terminalpath, index = False, header = True, escapechar=' ')
chances.to_csv(chancepath, index = False, header = True, escapechar=' ')

print('Execution time: ', time.time() - t0)

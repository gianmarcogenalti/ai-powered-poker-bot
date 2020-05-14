import time
import pandas as pd
from Parsing.dataframeparsing import infosetdf, nodesdf
from Parsing.df_reinforcement import *
from Parsing.probabilities import *

def parsing(game = 'leduc5', verbose = False, tocsv = False):

    t0 = time.time()

    game_for_csv = game

    game = 'Parsing\\input - ' + game + '.txt' # Game to play
     # name to use on the .csv file
    if verbose:
        print('Chosen game: ', game_for_csv, '\n')
    ## Path to store the .csv files and names of the files

    path = '..\\Import-files'
    infopath = path + '\\' + game_for_csv + '_infosets.csv'
    nodespath = path + '\\' + game_for_csv + '_nodes.csv'

    ## Creating dataframes

    infosets = infosetdf(game) ## Infosets dataframe: 'History',
                                # 'Members' (histories of nodes that compose the infoset),
                                # 'Depth' (number of moves to reach the infoset)
    if verbose:
        print('infosets created!\n')

    nodes = nodesdf(game) ## Full nodes dataframe: 'History', 'Type' (typology of the node)
    if verbose:
        print('nodes created!\n')

    ## Reinforcing dataframes with additional informations

    nodesdepth(nodes)# adding the "parents" of a node: all the nodes from which the node is reachable
    if verbose:
        print('depth added to nodes!\n')

    maptois(nodes, infosets) # adding a map that sends a node to the infoset he belongs using dataframe indices
    if verbose:
        print('map to infosets added to nodes!\n')

    payoffdescendents(nodes, infosets) # adding the "sons" of a node: all the nodes reachable moving forward from the node,
    if verbose:
        print('sons added to nodes!\n') # also adding the payoff vector of a node
        print('payoff vectors added to nodes!\n')
        print('payoff vectors added to infosets!\n')

    directsons(nodes) # adding vector of "direct sons" of a node
    if verbose:
        print('direct sons added to nodes!\n')

    indexmembers(infosets, nodes) # same of the 'Members' column but using the indices of the 'nodes' dataframe
    if verbose:
        print('indexed members added to infosets!\n')

    nodeantenates(nodes) # adding the parents of a node
    directparent(nodes, infosets)
    if verbose:
        print('parents added to nodes!\n')

    isplayers(infosets, nodes) # adding the player that moves in the infoset
    if verbose:
        print('players added to infosets!\n')

    descendents(infosets) # adding the "sons" of an infoset: all the infosets reachable moving forward from the infoset
    alldescendents(infosets)
    #isdirectsons(infosets,nodes)
    if verbose:
        print('sons added to infosets!\n')

    antenates(infosets) # adding the "parents" of an infoset: all the infosets from which the infoset is reachable
    directantenates(infosets)
    if verbose:
        print('parents added to infosets!\n')

    isactions(infosets,nodes) # adding possible actions to an infoset using the map with  nodes
    if verbose:
        print('actions added to infosets!\n')

    update_nodeprob(nodes) # adding probabilities of chance nodes
    if verbose:
        print('probabilities added to nodes!\n')

    update_infoprob(infosets,nodes) # updating infosets' probabilities by sum of nodes' Probabilities
    if verbose:
        print('infosets probabilities updated!')

    #prob_leaf(nodes)
    if verbose:
        print(nodes)

    #prob_check(nonterminals)

    ## Writing dataframes on a tre and on a .csv file
    #nodestree = totree(nodes)
    if tocsv:
        infosets.to_csv(infopath, index = False, header = True, escapechar=' ')
        nodes.to_csv(nodespath, index = False, header = True, escapechar=' ')
    if verbose:
        print('Parsing Execution time: ', time.time() - t0)

    return nodes,infosets

parsing("leduc3")

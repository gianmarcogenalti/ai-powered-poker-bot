import pandas as pd
from dataframeparsing import *
from df_reinforcement import *

kuhn = 'input - kuhn.txt'
l3 = 'input - leduc3.txt'
l5 = 'input - leduc5.txt'

game = l3
game_for_csv = "leduc3"

path = 'C:\\Users\\gianm\\Documents\\POKERBOT\\Import_files'
infopath = path + '\\' + game_for_csv + '_infosets.csv'
nonterminalpath = path + '\\' + game_for_csv + '_nonterminals.csv'
terminalpath = path + '\\' + game_for_csv + '_terminals.csv'
chancepath = path + '\\' + game_for_csv + '_chances.csv'

## Creating dataframes

chances = chancedf(game)

infosets = infosetdf(game)

terminals = terminaldf(game)

nonterminals = nonterminaldf(game)

## Reinforcing Infosets dataframes

payoffvectors(infosets,terminals)
isplayers(infosets, nonterminals)
descendents(infosets)
antenates(infosets)

#print(infosets)

## Writing output on a .csv file

infosets.to_csv(infopath, index = False, header = True)
nonterminals.to_csv(nonterminalpath, index = False, header = True)
terminals.to_csv(terminalpath, index = False, header = True)
chances.to_csv(chancepath, index = False, header = True)

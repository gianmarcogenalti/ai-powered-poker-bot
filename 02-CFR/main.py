from loaddata2 import *
from abstractpreparation import *
from Vanilla_Gamer import *
from MC_Gamer import *
from trees2 import *

# Choose game:

game = "leduc3"

# Loads the csv and gets the proper infosets
infosets = loadinfosets(game)
abs_infosets = loadabstract(game)
nodes    = loadnodes(game)
# Enriching the nodes and abstract infosets dataframe
update_nodeprob(nodes)
maptoclust(infosets, abs_infosets)
abstractnodes(nodes, abs_infosets, infosets)
abstractsons(nodes, abs_infosets, infosets)
abstractdads(abs_infosets)
abs_depth(abs_infosets)
'''
for i in range(len(abs_infosets.index)):
    print(abs_infosets.Dads[i])
    print(abs_infosets.Direct_Sons[i])
'''
# Environment set
T = 100
method = 'vanilla'

monkey = Vanilla_Gamer(abs_infosets, nodes)
monkey.train(T)
monkey.print_output(game, infosets)

for i in range(len(monkey.strategies)):
    print(monkey.strategies[i])
'''
hopper = MC_Gamer(abs_infosets, nodes)
print(hopper.infosets.Payoff_P1)



## Tree rendering

#nodestree(nodes, "probability")
'''
get_back(infosets, monkey.strategies)
filename = game + "_infosets.csv"
infosets.to_csv(filename, index = False, header = True, escapechar=' ')
'''

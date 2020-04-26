from loaddata import *
from clusterinfosets import *

# Choose game:

#game = "kuhn"
#game = "leduc3"
game = "leduc3"

# Loads the csv and gets the proper infoset
infosets, rawinfosets = loadinfosets(game)

# Merges infosets without loss of information
infosets = cluster(infosets, infoloss = False)

print(infosets)
#infosets.to_csv("..\\Import-files\\ph1_"+game+".csv", index = False, header = True)

# Properly clusters infosets
infosets = cluster(infosets, infoloss = True)

print(infosets)
infosets.to_csv("..\\Import-files\\clust_"+game+".csv", index = False, header = True)
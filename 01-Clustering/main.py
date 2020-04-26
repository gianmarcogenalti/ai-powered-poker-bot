from loaddata import *
from clusterinfosets import *

# Choose game:

game = "leduc5"

# Loads the csv and gets the proper infoset
infosets, rawinfosets = loadinfosets(game)

print(infosets)
# Merges infosets without loss of information
infosets = cluster(infosets, infoloss = False)

print(infosets)
#infosets.to_csv("..\\Import-files\\ph1_"+game+".csv", index = False, header = True)

# Properly clusters infosets
infosets = cluster(infosets, infoloss = True)

print(infosets)

# Collects the initial data left behind
infosets = infosetstoprint(infosets,rawinfosets)

# Saves it
infosets.to_csv("..\\Import-files\\clust_"+game+".csv", index = False, header = True)
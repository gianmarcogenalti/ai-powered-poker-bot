import sys
import time
import Parsing as parser
import Clustering as abstraction
import CFR as blueprint
import Subgames as sr

game = "leduc5" # sys.argv[1]

try:
    cfrmethod = sys.argv[2]
except:
    cfrmethod = 'vanilla'
try:
    cfrT = int(sys.argv[3])
except:
    cfrT = 100
try:
    cfrverbose = sys.argv[4]
except:
    cfrverbose = True

t0 = time.time()
nodes, infosets = parser.parsing(game, verbose = False)
t1 = time.time()
print("Parsing : Done in %f seconds" % (t1 - t0))
abs_infosets = abstraction.abstractgeneration(infosets, verbose = False)
t2 = time.time()
print("Abstract Generation : Done in %f seconds" % (t2 - t1))
infosets, abs_infosets = blueprint.cfr(nodes, infosets, abs_infosets, game, method = cfrmethod, T = cfrT, verbose = cfrverbose)
t3 = time.time()
print("Blueprint Strategy : Done in %f seconds" % (t3 - t2))
sr.subgameresolver(nodes, infosets, abs_infosets)
t4 = time.time()
print("Subgames Resolved : Done in %f seconds" % (t4 - t3))


#for index, row in nodes.iterrows():
    #print(row)





tf = time.time()
print("Total Execution time: %d" % (tf - t0))

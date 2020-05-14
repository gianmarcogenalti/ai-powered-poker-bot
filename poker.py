import sys
import time
import Parsing as parser
import Clustering as abstraction
import CFR as blueprint

game = sys.argv[1]

t0 = time.time()
nodes, infosets = parser.parsing(game)
t1 = time.time()
print("Parsing : Done in %d" % (t1 - t0))
abs_infosets = abstraction.abstractgeneration(infosets)
t2 = time.time()
print("Abstract Generation : Done in %d" % (t2 - t1))
infosets, abs_infosets = blueprint.cfr(nodes, infosets, abs_infosets, game, method = 'vanilla', T = 100, verbose = True)
t3 = time.time()
print("Blueprint Strategy : Done in %d" % (t3 - t2))




tf = time.time()
print("Total Execution time: %d" % (tf - t0))

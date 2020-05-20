import sys
import time
import Parsing as parser
import Clustering as abstraction
import CFR as blueprint
import Subgames as sr
import NodeCFR as ncfr
import Printer as printer

game =  sys.argv[1]

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
nodes, abs_infosets, roots, leaves, players = sr.subgamegeneration(nodes, infosets, abs_infosets, limited = True)
t4 = time.time()
print("Subgames Generated : Done in %f seconds" % (t4 - t3))
output = ncfr.subgameresolver(nodes, infosets, abs_infosets, roots, leaves, players, method = 'chance_sampling', T = 100)
t5 = time.time()
print("Subgames Resolved : Done in %f seconds" % (t5 - t4))
printer.print_output(game, output, infosets, abs_infosets)


tf = time.time()
print("Total Execution time: %d" % (tf - t0))

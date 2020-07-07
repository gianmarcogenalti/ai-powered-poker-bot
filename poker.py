import sys
import time
import Parsing as parser
import Clustering as abstraction
import CFR as blueprint
import Subgames as sr
import NodeCFR as ncfr
import Printer as printer
import pandas as pd

# game =  "leduc3" #sys.argv[1]
game = sys.argv[1]

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
#
gamenodes = 'nodes - ' + game + '.pkl'
gameinfosets = 'infosets - ' + game + '.pkl'
try:
    nodes = pd.read_pickle(gamenodes)
    infosets = pd.read_pickle(gameinfosets)
    print('by pickle')
except:
    nodes, infosets = parser.parsing(game, verbose = False)
    nodes.to_pickle(gamenodes)
    infosets.to_pickle(gameinfosets)
t1 = time.time()
print("Parsing : Done in %f seconds" % (t1 - t0))
<<<<<<< HEAD
#
abs_infosets = abstraction.abstractgeneration(infosets, verbose = False)
=======
abs_infosets = abstraction.abstractgeneration(infosets, verbose = False, sizeofabstraction = 0.95)
>>>>>>> fe49a8827202e09c0f1597a99de55e7d804147fb
t2 = time.time()
print("Abstract Generation : Done in %f seconds" % (t2 - t1))
#
infosets, abs_infosets = blueprint.cfr(nodes, infosets, abs_infosets, game, method = cfrmethod, T = cfrT, verbose = cfrverbose)
t3 = time.time()
print("Blueprint Strategy : Done in %f seconds" % (t3 - t2))
printer.print_output_bp(game+'bp', infosets, abs_infosets)
#
nodes, abs_infosets, roots, leaves, players = sr.subgamegeneration(nodes, infosets, abs_infosets, limited = True)
t4 = time.time()
print("Subgames Generated : Done in %f seconds" % (t4 - t3))
#
output = ncfr.subgameresolver(nodes, infosets, abs_infosets, roots, leaves, players, method = 'chance_sampling', T = 1000)
t5 = time.time()
print("Subgames Resolved : Done in %f seconds" % (t5 - t4))
printer.print_output(game, output, infosets, abs_infosets)


tf = time.time()
print("Total Execution time: %d" % (tf - t0))

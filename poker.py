import sys
import time
import Parsing as parser
import argparse
import Clustering as abstraction
import CFR as blueprint
import NodeCFR as nodeblueprint
import Subgames as sr
import SubgameCFR as ncfr
import Printer as printer
import pandas as pd

# game =  "leduc3" #sys.argv[1]

ap = argparse.ArgumentParser()
ap.add_argument("-g", "--game", default = 'leduc3')
ap.add_argument('-a', '--abstraction', default = 0.75)
ap.add_argument('-bp', '--blueprint', default = 1)
ap.add_argument("-m1", "--method1", default = 'public_chance')
ap.add_argument("-i1", "--iteration1", default = 1000)
ap.add_argument('-dl', '--depthlim', default = 1)
ap.add_argument("-m2", "--method2", default = 'public_chance')
ap.add_argument("-i2", "--iteration2", default = 1000)
ap.add_argument('-v', '--verbose', default = 1)

args = vars(ap.parse_args())
print(args)

t0 = time.time()
#
if int(args['blueprint']):
    try:
        nodes = pd.read_pickle('nodes - ' + args['game'] + '.pkl')
        infosets = pd.read_pickle('infosets - ' + args['game']  + '.pkl')
        print('by pickle')
    except:
        nodes, infosets = parser.parsing(args['game'] , verbose = args['verbose'])
        nodes.to_pickle('nodes - ' + args['game'] + '.pkl')
        infosets.to_pickle('infosets - ' + args['game']  + '.pkl')
    t1 = time.time()
    print("Parsing : Done in %f seconds" % (t1 - t0))
    abs_infosets = abstraction.abstractgeneration(infosets, verbose = int(args['verbose']), sizeofabstraction = float(args['abstraction']))
    t2 = time.time()
    print("Abstract Generation : Done in %f seconds" % (t2 - t1))
    n_abstract = len(abs_infosets.index)
    #
    n_nodes = len(nodes.index)
    infosets, abs_infosets = nodeblueprint.nodecfr(nodes, infosets, abs_infosets, args['game'], method = args['method1'], T = int(args['iteration1']), verbose = int(args['verbose']))
    t3 = time.time()
    print("Blueprint Strategy : Done in %f seconds" % (t3 - t2))
    #
    printer.print_output_bp(args['game']+'bp', infosets, abs_infosets)
    abs_infosets = abs_infosets.head(n_abstract)
    nodes = nodes.head(n_nodes)
    #
    nodes.to_pickle('nodes - '+ args['game'] +'bp'+'.pkl')
    infosets.to_pickle('infosets - '+ args['game'] +'bp'+'.pkl')
    abs_infosets.to_pickle('abs_infosets - '+ args['game'] +'bp'+'.pkl')
else:
    try:
        nodes = pd.read_pickle('nodes - '+ args['game'] +'bp'+'.pkl')
        infosets = pd.read_pickle('infosets - '+ args['game'] +'bp'+'.pkl')
        abs_infosets = pd.read_pickle('abs_infosets - '+ args['game'] +'bp'+'.pkl')
    except:
        raise NotImplementedError("There are not pre-computed blueprint strategies for this game, set --blueprint argument to True to compute them.")
    n_abstract = len(abs_infosets.index)
    #print(abs_infosets.head(n_abstract))
    print('Infosets reduced by %f percent!' % (1-n_abstract/len(infosets.index)))
    print('Found a pre-computed blueprint strategy!')
    t3 = t0

nodes, abs_infosets, roots, leaves, players = sr.subgamegeneration(nodes, infosets, abs_infosets, limited = int(args['depthlim']))
t4 = time.time()
print("Subgames Generated : Done in %f seconds" % (t4 - t3))
#
output = ncfr.subgameresolver(nodes, infosets, abs_infosets, roots, leaves, players, method = args['method2'], T = int(args['iteration2']))
t5 = time.time()
print("Subgames Resolved : Done in %f seconds" % (t5 - t4))
printer.print_output(args['game'] , output, infosets, abs_infosets)


tf = time.time()
print("Total Execution time: %d" % (tf - t0))

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
import Exploiter as E
import Utilities as U
import pandas as pd
import pickle

# game =  "leduc3" #sys.argv[1]

ap = argparse.ArgumentParser()
ap.add_argument("-g", "--game", default = 'leduc3')
ap.add_argument('-a', '--abstraction', default = 0.76)
ap.add_argument('-bp', '--blueprint', default = 1)
ap.add_argument("-m1", "--method1", default = 'public_chance')
ap.add_argument("-i1", "--iteration1", default = 1000)
ap.add_argument('-dl', '--depthlim', default = 1)
ap.add_argument("-m2", "--method2", default = 'public_chance')
ap.add_argument("-i2", "--iteration2", default = 1000)
ap.add_argument('-d', '--depth', default = 5)
ap.add_argument('-sg', '--subgames', default = 1)
ap.add_argument('-dt', '--depththreshold', default = 1)
ap.add_argument('-v', '--verbose', default = 1)
ap.add_argument('-o1', '--onlyfirstplayer', default = 0)

args = vars(ap.parse_args())
print(args)

t0 = time.time()
#
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
#
#print(len(infosets.index), len(nodes.index))
try:
    abs_infosets = pd.read_pickle('abs_infosets - '+ args['game'] + str(int(float(args['abstraction'])*100)) + '.pkl')
    print('by pickle')
except:
    abs_infosets = abstraction.abstractgeneration(infosets, verbose = int(args['verbose']), sizeofabstraction = float(args['abstraction']), onlyfirstplayer = int(args["onlyfirstplayer"]))
    abs_infosets.to_pickle('abs_infosets - '+ args['game'] + str(int(float(args['abstraction'])*100)) + '.pkl')
t2 = time.time()
print("Abstract Generation : Done in %f seconds" % (t2 - t1))
n_abstract = len(abs_infosets.index)
n_nodes = len(nodes.index)
#
if int(args['blueprint']):
    infosets, abs_infosets= nodeblueprint.nodecfr(nodes, infosets, abs_infosets, args['game'], method = args['method1'], T = int(args['iteration1']), verbose = int(args['verbose']))
    t3 = time.time()
    print("Blueprint Strategy : Done in %f seconds" % (t3 - t2))
    #
    printer.print_output_bp(args['game']+'bp'+str(int(float(args['abstraction'])*100)), infosets, abs_infosets)
    #
    nodes.to_pickle('nodes - '+ args['game'] +'bp'+str(int(float(args['abstraction'])*100))+'.pkl')
    infosets.to_pickle('infosets - '+ args['game'] +'bp'+str(int(float(args['abstraction'])*100))+'.pkl')
    abs_infosets.to_pickle('abs_infosets - '+ args['game'] +'bp'+str(int(float(args['abstraction'])*100))+'.pkl')
else:
    try:
        nodes = pd.read_pickle('nodes - '+ args['game'] +'bp'+str(int(float(args['abstraction'])*100))+'.pkl')
        infosets = pd.read_pickle('infosets - '+ args['game'] +'bp'+str(int(float(args['abstraction'])*100))+'.pkl')
        abs_infosets = pd.read_pickle('abs_infosets - '+ args['game'] +'bp'+str(int(float(args['abstraction'])*100))+'.pkl')
    except:
        raise NotImplementedError("There are not pre-computed blueprint strategies for this game, set --blueprint argument to True to compute them.")
    print('Found a pre-computed blueprint strategy!')
    t3 = t0
print(E.exploiter(nodes, abs_infosets.Actions_Prob, nodes.index[-1], 1),E.exploiter(nodes, abs_infosets.Actions_Prob, nodes.index[-1], 2),E.value_of_the_game(nodes,abs_infosets.Actions_Prob, nodes.index[-1]))
abs_infosets = abs_infosets.head(n_abstract)
nodes = nodes.head(n_nodes)
if int(args['subgames']):
    nodes, infosets, abs_infosets, roots, leaves, players = sr.subgamegeneration(nodes, infosets, abs_infosets, limited = int(args['depthlim']), max_depth = int(args['depth']))
    t4 = time.time()
    print("Subgames Generated : Done in %f seconds" % (t4 - t3))
    #
    output = ncfr.subgameresolver(nodes, infosets, roots, leaves, players, depththreshold = int(args['depththreshold']), method = args['method2'], T = int(args['iteration2']))
    t5 = time.time()
    print("Subgames Resolved : Done in %f seconds" % (t5 - t4))
    with open('finalstrategy - '+args['game']+str(int(float(args['abstraction'])*100))+'.pkl', 'wb') as handle:
        pickle.dump(output, handle, protocol=pickle.HIGHEST_PROTOCOL)
else:
    try:
        with open('finalstrategy - '+args['game']+str(int(float(args['abstraction'])*100))+'.pkl', 'rb') as handle:
            output = pickle.load(handle)
    except:
        nodes, infosets, abs_infosets, roots, leaves, players = sr.subgamegeneration(nodes, infosets, abs_infosets, limited = int(args['depthlim']), max_depth = int(args['depth']))
        t4 = time.time()
        print("Subgames Generated : Done in %f seconds" % (t4 - t3))
        #
        output = ncfr.subgameresolver(nodes, infosets, roots, leaves, players, depththreshold = int(args['depththreshold']), method = args['method2'], T = int(args['iteration2']))
        t5 = time.time()
        print("Subgames Resolved : Done in %f seconds" % (t5 - t4))
        with open('finalstrategy - '+args['game']+str(int(float(args['abstraction'])*100))+'.pkl', 'wb') as handle:
            pickle.dump(output, handle, protocol=pickle.HIGHEST_PROTOCOL)

nodes = nodes.head(n_nodes)
U.nodetoclust(nodes, infosets, abs_infosets)            
printer.print_output(args['game'] , infosets)

print(E.exploiter(nodes, output, nodes.index[-1], 1, trueinfo = 1),E.exploiter(nodes, output, nodes.index[-1], 2, trueinfo = 1),E.value_of_the_game(nodes,output, nodes.index[-1], trueinfo = 1))

#with open('finalstrategy - '+args['game']+'.pkl', 'rb') as handle:
#    b = pickle.load(handle)

tf = time.time()
print("Total Execution time: %d" % (tf - t0))

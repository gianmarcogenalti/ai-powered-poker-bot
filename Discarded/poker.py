from gamesimulator import *

play,name = initialization()
while play:
    play = lets_play(name)
if not play and name == "noname":
    print(simulate_matches())

print("\n\n\n\n\n\n\nThank You!")

    '''
    infosets, abs_infosets = blueprint.cfr(nodes, infosets, abs_infosets, game, method = cfrmethod, T = cfrT, verbose = cfrverbose)
    t3 = time.time()
    print("Blueprint Strategy : Done in %f seconds" % (t3 - t2))
    printer.print_output_bp(game+'bp', infosets, abs_infosets)
    '''

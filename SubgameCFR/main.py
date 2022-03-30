import Utilities as U
from SubgameCFR.CSGamer import *
from SubgameCFR.VanillaGamer import *
from SubgameCFR.VanillaGamerPlus import *

def subgameresolver(nodes, abs_infosets, roots, leaves,players, depththreshold, method = 'public_chance', T = 100):
    if method == 'public_chance':
        output = dict()
        for i in range(len(abs_infosets.index)):
            output.update({i : abs_infosets.Actions_Prob[i]})
        for it in range(len(roots)):
            if nodes.Depth[nodes.index[-(len(roots)-it)]] >= depththreshold:
                try:
                    chance_sampling_cfr = CSGamer(nodes,abs_infosets, roots, leaves, players,it)
                    chance_sampling_cfr.run(iterations = T)
                    chance_sampling_cfr.compute_nash_equilibrium()
                    for t in roots[it]:
                        output.update({t : chance_sampling_cfr.nash_equilibrium[t]})
                except:
                    pass
        return output

import numpy as np
from CFR.Gamer import *
import time
import numpy as np
import math
'''
def init_n_actions(strategies):
    ret = 0
    for i in strategies:
        ret += len(i)
    return ret
'''
class MC_Gamer(Gamer):

    def __init__(self, infosets, nodes, verbose) :
        super().__init__(infosets, nodes, verbose)
        self.utilities   = np.zeros(len(self.infosets.index))
        self.cfutilities = [[] for _ in range(len(self.infosets.index))]
        self.root = -1
        #self.Probability_Opp = [0.0 for _ in range(len(self.infosets.index))]
        #self.Probability_P1 = [0.0 for _ in range(len(self.infosets.index))]
        #self.Probability_P2 = [0.0 for _ in range(len(self.infosets.index))]
        #self.cumpayoff = [0.0 for _ in range(len(self.infosets.index))]
        #self.n_actions = init_n_actions(self.strategies)
        self.proxy = [np.zeros(len(self.strategies[_])) for _ in range(len(self.strategies))]
################################################################################
    def train(self, T):
        t0 = time.time()
        while self.t < T:
                self.waterlilies_select(1)
                #print("The first frog selected the waterlilies!")
                self.waterlilies_jumps(2)
                #print("The second frog jumped on the waterlilies!")
                self.waterlilies_select(2)
                #print("The second frog selected other waterlilies!")
                self.waterlilies_jumps(1)
                #print("The first frog jumped on the other waterlilies!")
                self.t += 1
                if not self.t % 10 and self.verbose:
                    print("The frogs had %d challenges!" % self.t)
        if self.verbose:
            print("After %d seconds the frogs got bored!" % (time.time() - t0))

################################################################################
    def get_regrets(self, absidx):
        regrets = []
        for act in range(len(self.infosets.Actions[absidx])):
            regrets.append(self.cfutilities[absidx][act] - self.utilities[absidx])
        return regrets

################################################################################
    def waterlilies_select(self, opponent):
        self.root = int(np.random.choice(range(len(self.infosets.index[self.infosets.Depth == 1]))))
        self.proxy = [np.zeros(len(self.strategies[_])) for _ in range(len(self.strategies))]
        opp_indices = self.infosets.index[self.infosets.Player == opponent]
        for idx in opp_indices:
            act_index = int(np.random.choice(range(len(self.strategies[idx])), 1))
            self.proxy[idx][act_index] = self.strategies[idx][act_index]

            indices = self.infosets.index[self.infosets.Player != opponent]
            for i in indices:
                self.proxy[i] = self.strategies[i]

################################################################################

    def waterlilies_jumps(self, player) :
        self.utilities   = np.zeros(len(self.infosets.index))
        self.cfutilities = [[] for _ in range(len(self.infosets.index))]
        #payoffsums = [0.0 for _ in range(len(self.infosets.index))]
        sign = 1 if player == 1 else -1
        player_indices = self.infosets.index[self.infosets.Player == player]
        terminals = []
        stopit = False
        for index in reversed(range(len(self.infosets.index))):
            if not stopit:
                if self.infosets.Depth[index] == 1:
                    index = self.root
                    stopit = True
                self.utilities[index] = 0.0
                for idlist in range(len(self.infosets.Direct_Sons[index])):
                    dslist = self.infosets.Direct_Sons[index][idlist]
                    if len(dslist) == 0:
                        if index in player_indices:
                            self.utilities[index] += self.infosets.Payoff_P1[index][idlist] * self.proxy[index][idlist] * sign
                            self.cfutilities[index].append(self.infosets.Payoff_P1[index][idlist] * sign)
                            terminals.append(index)
                        elif self.proxy[index][idlist] > 0.:
                            self.utilities[index] += self.infosets.Payoff_P1[index][idlist]
                            self.cfutilities[index].append(self.infosets.Payoff_P1[index][idlist])
                    else:
                        self.cfutilities[index].append(0)
                        if index in player_indices:
                            for idson in range(len(dslist)):
                                ds = dslist[idson]
                                self.utilities[index] += self.utilities[ds] * self.proxy[index][idlist] * self.infosets.Nature_Weight[index][idlist][idson] * sign
                                self.cfutilities[index][idlist] += self.utilities[ds] * self.infosets.Nature_Weight[index][idlist][idson] * sign
                        elif self.proxy[index][idlist] > 0.:
                            for idson in range(len(dslist)):
                                ds = dslist[idson]
                                self.utilities[index] += self.utilities[ds] * self.infosets.Nature_Weight[index][idlist][idson]
                                self.cfutilities[index][idlist] += self.utilities[ds] * self.infosets.Nature_Weight[index][idlist][idson]

        for t in terminals:
            regrets = self.get_regrets(t)
            self.update_strategies(t, regrets)
################################################################################

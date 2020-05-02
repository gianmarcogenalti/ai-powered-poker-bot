import numpy as np
from Gamer import *
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

    def __init__(self, infosets, nodes) :
        super().__init__(infosets, nodes)
        self.utilities   = np.zeros(len(self.infosets.index))
        self.cfutilities = [[] for _ in range(len(self.infosets.index))]
        self.Probability_Opp = [0.0 for _ in range(len(self.infosets.index))]
        self.Probability_P1 = [0.0 for _ in range(len(self.infosets.index))]
        self.Probability_P2 = [0.0 for _ in range(len(self.infosets.index))]
        #self.n_actions = init_n_actions(self.strategies)
        self.proxy = [np.zeros(len(self.strategies[_])) for _ in range(len(self.strategies))]
################################################################################
    def train(self, T):
        t0 = time.time()
        while self.t < T:
            self.tree_drop()
            print("The monkey dropped from the tree!")
            self.tree_climb()
            self.t += 1
            print("The monkey climbed the tree %d times!" % self.t)
        print("After %d seconds the monkey got bored!" % (time.time() - t0))

################################################################################
    def get_regrets(self, absidx):
        regrets = []
        for act in range(len(self.infosets.Actions[absidx])):
            regrets.append(self.cfutilities[absidx][act] - self.utilities[absidx])
        return regrets

################################################################################
    def tree_drop(self) : ## Top-Bottom of the tree
        roots = self.infosets.index[self.infosets.Depth == 1]
        #first = True
        for startingidx in roots:
            #self.recursive_probs_abstract_call(startingidx, init = first)
            self.recursive_probs_oppo_abstract_call(startingidx, init = True)
            #first = False
        print(self.Probability_Opp)

    def tree_climb(self) :
        payoffsums = [0.0 for _ in range(len(self.infosets.index))]

################################################################################
    def sample_actions(self, n_samples, opponent):
        self.proxy = [np.zeros(len(self.strategies[_])) for _ in range(len(self.strategies))]
        depths = self.infosets.Depth[self.infosets.Player == opponent]
        #print(depths)
        for dpt in depths:
            n_samples_dpt = math.ceil(n_samples*(len(self.infosets[self.infosets.Depth == dpt])/len(self.infosets.index)))
            #print(n_samples_dpt)
            for i in range(n_samples_dpt):
                abs_index = int(np.random.choice(self.infosets.index[(self.infosets.Player == opponent) & (self.infosets.Depth == dpt)], 1))
                #print(abs_index)
                act_index = int(np.random.choice(range(len(self.strategies[abs_index])), 1))
                #print(act_index)
                self.proxy[abs_index][act_index] = self.strategies[abs_index][act_index]

            indices = self.infosets.index[self.infosets.Player != opponent]
            for i in indices:
                self.proxy[i] = self.strategies[i]
################################################################################

    def get_terminals(self):
        payoff = [0.0 for _ in range(len(self.infosets.index))]
        for depth in range(1,max(self.infosets['Depth']) + 1):
            icurinfosets = list(self.infosets.index[self.infosets['Depth'] == depth])
            for icurinfo in icurinfosets :
                dslists = self.infosets.Direct_Sons[icurinfo]
                for idslist in range(len(dslists)) : # select one action
                    dslist = dslists[idslist]
                    if self.proxy[icurinfo][idslist] > 0.0:
                        if len(dslist) == 0:
                            payoff[icurinfo] += self.infosets.Payoff_P1[icurinfo][idslist]*sign*(1/self.Probability_Opp[icurinfo])
                        else:
                            for idson in range(len(dslist)) : # select one son infoset
                                dson = dslist[idson]
                                if self.infosets.Player[icurinfo] == 1 :
                                    self.Probability_P1[dson] += self.Probability_P1[icurinfo] * self.strategies[icurinfo][idslist] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                                    self.Probability_P2[dson] += self.Probability_P2[icurinfo] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                                else :
                                    self.Probability_P2[dson] += self.Probability_P2[icurinfo] * self.strategies[icurinfo][idslist] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                                    self.Probability_P1[dson] += self.Probability_P1[icurinfo] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                                if self.infosets.Player[dson] == 1 :
                                    self.Probability_Opp[dson] = self.Probability_P2[dson]
                                else :
                                    self.Probability_Opp[dson] = self.Probability_P1[dson]

        print(terminals)


################################################################################
    # Infosets Opponents probabilities

    def tree_drop(self, proxy = False) :
        if proxy:
            strat = self.proxy
            self.terminals = []
        else:
            strat = self.strategies
        self.Probability_Opp = [0.0 for _ in range(len(self.infosets.index))]
        self.Probability_P1 = [0.0 for _ in range(len(self.infosets.index))]
        self.Probability_P2 = [0.0 for _ in range(len(self.infosets.index))]
        roots = self.infosets.index[self.infosets.Depth == 1]
        for startingidx in roots:
            tot_p = 0
            for im in self.infosets.Index_Members[startingidx]:
                tot_p += self.nodes.Nature_Prob[im]
            self.Probability_Opp[startingidx] = tot_p
            self.Probability_P1[startingidx] = tot_p
            self.Probability_P2[startingidx] = tot_p
        for depth in range(1,max(self.infosets['Depth']) + 1):
            icurinfosets = list(self.infosets.index[self.infosets['Depth'] == depth])
            for icurinfo in icurinfosets :
                dslists = self.infosets.Direct_Sons[icurinfo]
                for idslist in range(len(dslists)) : # select one action
                    dslist = dslists[idslist]
                    for idson in range(len(dslist)) : # select one son infoset
                        dson = dslist[idson]
                        if self.infosets.Player[icurinfo] == 1 :
                            self.Probability_P1[dson] += self.Probability_P1[icurinfo] * strat[icurinfo][idslist] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                            self.Probability_P2[dson] += self.Probability_P2[icurinfo] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                        else :
                            self.Probability_P2[dson] += self.Probability_P2[icurinfo] * strat[icurinfo][idslist] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                            self.Probability_P1[dson] += self.Probability_P1[icurinfo] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                        if self.infosets.Player[dson] == 1 :
                            self.Probability_Opp[dson] = self.Probability_P2[dson]
                        else :
                            self.Probability_Opp[dson] = self.Probability_P1[dson]

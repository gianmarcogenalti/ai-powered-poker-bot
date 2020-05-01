import numpy as np
from Gamer import *
import time
import numpy as np

def init_n_actions(strategies):
    ret = 0
    for i in strategies:
        ret += len(i)
    return ret

class MC_Gamer(Gamer):

    def __init__(self, infosets, nodes) :
        super().__init__(infosets, nodes)
        self.utilities   = np.zeros(len(self.infosets.index))
        self.cfutilities = [[] for _ in range(len(self.infosets.index))]
        self.Probability_Opp = [0.0 for _ in range(len(self.infosets.index))]
        self.n_actions = init_n_actions(self.strategies)
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
        proxy = [np.zeros(len(self.strategies[_])) for _ in range(len(self.strategies))]
        for i in range(n_samples):
            abs_index = int(np.random.choice(self.infosets.index[self.infosets.Player == opponent], 1))
            print(abs_index)
            act_index = int(np.random.choice(range(len(self.strategies[abs_index])), 1))
            print(act_index)
            proxy[abs_index][act_index] = self.strategies[abs_index][act_index]

        indices = self.infosets.index[self.infosets.Player != opponent]
        for i in indices:
            proxy[i] = self.strategies[i]

        return proxy

    def get_terminals(self, proxy):
        reachables = []
        cumpayoff = [0.0 for _ in range(len(self.infosets.index))]
        terminals = []
        def recursive_terminals(idxucurnode):
            dslists = self.infosets[idxcurnode].Direct_Sons
            for idlist in range(len(dslists)):
                dslist = dslists[idlist]
                if proxy[idlist] > 0.0:
                    if len(dslist) > 0:
                        for idson in range(len(dslist)):
                            son = dslist[idson]
                            reachables.append(idson)
                            recursive_terminals(idson)
                    else:
                        if idxcurnode not in terminals:
                            terminals.append(idxcurnode)
                        cumpayoff[idxcurnode] += self.infosets.[idxcurnode]




################################################################################
    # Infosets Opponents probabilities

    def recursive_probs_oppo_abstract_call(self, startingnodeidx, init = False) :

        if init :
            self.Probability_Opp = [0.0 for _ in range(len(self.infosets.index))]

            tot_p = 0
            for im in self.infosets.Index_Members[startingnodeidx]:
                tot_p += self.nodes.Nature_Prob[im]
            self.Probability_Opp[startingnodeidx] = tot_p

        def recursive_probs_oppo_abstract(idxcurnode, prevprob = 1) :
            dslists = self.infosets.Direct_Sons[idxcurnode]
            for idslist in range(len(dslists)) : # select one action
                if len(dslists) > 0 :
                    dslist = dslists[idslist]
                    if len(dslist) > 0 :
                        for idson in range(len(dslist)) : # select one son infoset
                            dson = dslist[idson]
                            prevprobnow = prevprob
                            if self.infosets.Player[idxcurnode] != selectplayer:
                                prevprobnow = prevprob * self.strategies[idxcurnode][idslist] * self.infosets.Nature_Weight[idxcurnode][idslist][idson]
                            if self.infosets.Player[dson] == selectplayer :
                                self.Probability_Opp[dson] += prevprobnow
                            recursive_probs_oppo_abstract(dson,prevprobnow)

        selectplayer = 1
        recursive_probs_oppo_abstract(startingnodeidx, prevprob = self.Probability_Opp[startingnodeidx])
        selectplayer = 2
        recursive_probs_oppo_abstract(startingnodeidx, prevprob = self.Probability_Opp[startingnodeidx])

import numpy as np
from Gamer import *
import time

class Vanilla_Gamer(Gamer):

    def __init__(self, infosets, nodes) :
        super().__init__(infosets, nodes)
        self.utilities   = np.zeros(len(self.infosets.index))
        self.cfutilities = [[] for _ in range(len(self.infosets.index))]
        self.Probability_Opp = [0.0 for _ in range(len(self.infosets.index))]
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
        #roots = self.infosets.index[self.infosets.Depth == 1]
        #first = True
        #for startingidx in roots:
            #self.recursive_probs_abstract_call(startingidx, init = first)
            #self.recursive_probs_oppo_abstract_call(startingidx, init = True)
            #first = False
        self.probs_oppo_abstract_call()
        print(self.Probability_Opp)

    def tree_climb(self) :
        self.utilities   = np.zeros(len(self.infosets.index))
        self.cfutilities = [[] for _ in range(len(self.infosets.index))]
        payoffsums = [0.0 for _ in range(len(self.infosets.index))]
        for dpt in reversed(range(1, max(self.infosets.Depth) + 1)):
            for index in self.infosets.index[self.infosets.Depth == dpt]:
                if self.infosets.Player[index] == 1:
                    sign = 1
                else:
                    sign = -1
                for idlist in range(len(self.infosets.Direct_Sons[index])):
                    dslist = self.infosets.Direct_Sons[index][idlist]
                    if len(dslist) == 0:
                        payoffsums[index] += self.infosets.Payoff_P1[index][idlist] * self.strategies[index][idlist]
                        self.utilities[index] += self.Probability_Opp[index]*self.strategies[index][idlist]*sign*self.infosets.Payoff_P1[index][idlist]
                        self.cfutilities[index].append(self.Probability_Opp[index]*sign*self.infosets.Payoff_P1[index][idlist])
                    else:
                        self.cfutilities[index].append(0)
                        for ds in dslist:
                            payoffsums[index] += payoffsums[ds] * self.strategies[index][idlist]
                            self.utilities[index] += self.Probability_Opp[index]*self.strategies[index][idlist]*sign*payoffsums[ds]
                            self.cfutilities[index][idlist] += self.Probability_Opp[index]*sign*payoffsums[ds]
                #print(self.infosets.History[index],self.utilities[index], self.strategies[index],self.cfutilities[index],"\n")
                regrets = self.get_regrets(index)
                self.update_strategies(index, regrets)


###############################################################################
# Infosets probabilities
    def recursive_probs_abstract_call(self, startingnodeidx, init = False) :

        if init :
            self.infosets.Probability =[0.0 for _ in range(len(self.infosets.index))]

            tot_p = 0
            for im in self.infosets.Index_Members[startingnodeidx]:
                tot_p += self.nodes.Nature_Prob[im]
            self.infosets.Probability[startingnodeidx] = tot_p

        def recursive_probs_abstract(idxcurnode, prevprob = 1) :
            dslists = self.infosets.Direct_Sons[idxcurnode]
            for idslist in range(len(dslists)) : # select one action
                if len(dslists) > 0 :
                    dslist = dslists[idslist]
                    if len(dslist) > 0 :
                        for idson in range(len(dslist)) : # select one infoset
                            dson = dslist[idson]
                            prevprobnow = prevprob * self.strategies[idxcurnode][idslist] * self.infosets.Nature_Weight[idxcurnode][idslist][idson]
                            self.infosets.Probability[dson] += prevprobnow
                            recursive_probs_abstract(dson,prevprobnow)

        recursive_probs_abstract(startingnodeidx, prevprob = self.infosets.Probability[startingnodeidx])
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
    
    def probs_oppo_abstract_call(self) : 
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
                            self.Probability_P1[dson] += self.Probability_P1[icurinfo] * self.strategies[icurinfo][idslist] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                            self.Probability_P2[dson] += self.Probability_P2[icurinfo]
                        else :
                            self.Probability_P2[dson] += self.Probability_P2[icurinfo] * self.strategies[icurinfo][idslist] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                            self.Probability_P1[dson] += self.Probability_P1[icurinfo]
                        if self.infosets.Player[dson] == 1 :
                            self.Probability_Opp[dson] = self.Probability_P2[dson]
                        else :
                            self.Probability_Opp[dson] = self.Probability_P1[dson]
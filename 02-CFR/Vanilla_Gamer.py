import numpy as np
from Gamer import *
import time

class Vanilla_Gamer(Gamer):

    def __init__(self, infosets, nodes) :
        super().__init__(infosets, nodes)
        self.utilities   = np.zeros(len(self.infosets.index))
        self.cfutilities = [[] for _ in range(len(self.infosets.index))]


################################################################################
    def tree_drop(self) : ## Top-Bottom of the tree
        t0 = time.time()
        roots = self.infosets.index[self.infosets.Depth == 1]
        first = True
        for startingidx in roots:
            self.recursive_probs_abstract_call(startingidx, init = first)
            firt = False
        print("The monkey dropped from the tree in ",time.time() - t0)

    def tree_climb(self) :
        payoffsums = np.zeros(len(self.infosets.index))
        for dpt in reversed(range(1, max(self.infosets.Depth) + 1)):
            for index, row in self.infosets[self.infosets.Depth == dpt].iterrows():
                if row.Player == 1:
                    sign = 1
                else:
                    sign = -1
                for idlist in range(len(row.Direct_Sons)):
                    dslist = row.Direct_Sons[idlist]
                    if len(dslist) == 0:
                        payoffsums[index] += row.Payoff_P1[idlist] * row.Actions_Prob
                        self.utilities[index] += row.Probability_Opp*row.Actions_Prob[idlist]*sign*row.Payoff_P1[idlist]
                        self.cfutilities[index].append(row.Probability_Opp*sign*row.Payoff_P1[idlist])
                    else:
                        for ds in action:
                            payoffsums[index] += payoffsums[ds] * row.Actions_Prob
                            self.utilities[index] += row.Probability_Opp*row.Actions_Prob[action]*sign*payoffsums[ds]
                            self.cfutilities[index].apppend(row.Probability_Opp*payoffsums[ds])
        print(self.utilities)

###############################################################################
    # Infosets probabilities
    def recursive_probs_abstract_call(self, startingnodeidx, prevprob = 1, init = False) :

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
                            prevprobnow = prevprob * self.infosets.Actions_Prob[idxcurnode][idslist] * self.infosets.Nature_Weight[idxcurnode][idslist][idson]
                            self.infosets.Probability[dson] += prevprobnow
                            recursive_probs_abstract(dson,prevprobnow)

        recursive_probs_abstract(startingnodeidx, prevprob = 1)
################################################################################

    def recursive_utility_call(self,startingabsidx):

        if init:
            self.utilities = np.zeros(len(self.infoset.index))

        if oppo_prob:
            prob = self.infosets.Probability_Opp
        else:
            prob = self.infosets.Probability

        def recursive_utility(absidx, sonut = 0) :
            dslists = self.infosets.Direct_Sons[absidx]
            for idslist in range(len(dslists)) :
                dslist = dslists[idslist]
                if len(dslist) == 0: ## so the action number idslist leads to terminal nodes aka a single abstract payoff
                    self.infosets.Exp_Utility[absidx] += self.infosets.Payoff_P1[idslist]*self.infosets.Actions_Prob[idslist]
                else:
                    for idson in range(len(dslist)): #cycling on sons
                        self.infosets.Exp_Utility[absidx] += self.infosets.Exp_Utility[idson]*self.infosets.Actions_Prob[idslist]
                        recursive_utility(idson, sonut)

        recursive_utility(startingabsidx)
'''
################################################################################
    def get_regrets(self, absidx):
        regrets = []
        for act in range(len(self.infosets.Actions[absidx])):
            regrets.append(self.infosets.Exp_CFUtility[absidx][act] - self.infosets.Exp_Utility[absidx])
        return regrets
###############################################################################




################################################################################
    def update_abstract(self, abs_index, regrets):
        self.update_strategies(abs_index, regrets)
        for i in self.infosets.Index_Members[abs_index]:
            self.nodes.Actions_Prob[i] = self.strategies[abs_index]
            self.recursive_probs(i)
            utility = 0.
            for son in self.nodes.Sons[i]:
                if self.nodes.Type[son] == 'L':
                    utility += self.nodes.Payoff_Vector_P1[son]*self.nodes.Probability[son]
            self.nodes.Exp_Utility[i] = utility
################################################################################
'''

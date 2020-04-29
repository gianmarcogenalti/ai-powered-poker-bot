import numpy as np
from Gamer import *
import time

class Vanilla_Gamer(Gamer):

    def __init__(self, infosets, nodes) :
        super().__init__(infosets, nodes)
        self.utilities   = [[] for _ in range(len(self.infosets.index))]
        self.cfutilities = [[] for _ in range(len(self.infosets.index))]


################################################################################
    def tree_drop(self) : ## Top-Bottom of the tree
        t0 = time.time()
        roots = self.infosets.index[self.infosets.Depth == 1]
        first = True
        for startingidx in roots:
            self.recursive_probs_abstract_call(startingidx, init = first)
            self.recursive_probs_oppo_abstract_call(startingidx, init = first)
            first = False
        print("The monkey dropped from the tree in ",time.time() - t0)
    '''
        def tree_climb(self) :
            for i in reversed(range(1, max(self.infosets.Depth)+1)):
    '''            

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
                            prevprobnow = prevprob * self.infosets.Actions_Prob[idxcurnode][idslist] * self.infosets.Nature_Weight[idxcurnode][idslist][idson]
                            self.infosets.Probability[dson] += prevprobnow
                            recursive_probs_abstract(dson,prevprobnow)

        recursive_probs_abstract(startingnodeidx, prevprob = self.infosets.Probability[startingnodeidx])
    ################################################################################
    # Infosets Opponents probabilities

    def recursive_probs_oppo_abstract_call(self, startingnodeidx, init = False) :

        if init :
            self.infosets.OppoProbability = [0.0 for _ in range(len(self.infosets.index))]
        
        tot_p = 0
        for im in self.infosets.Index_Members[startingnodeidx]:
            tot_p += self.nodes.Nature_Prob[im]
        self.infosets.OppoProbability[startingnodeidx] = tot_p

        def recursive_probs_oppo_abstract(idxcurnode, prevprob = 1) :
            dslists = self.infosets.Direct_Sons[idxcurnode]
            for idslist in range(len(dslists)) : # select one action
                if len(dslists) > 0 :
                    dslist = dslists[idslist]
                    if len(dslist) > 0 :
                        for idson in range(len(dslist)) : # select one son infoset
                            dson = dslist[idson]
                            prevprobnow = prevprob
                            if self.infosets.Player[idxcurnode] != selectplayer :
                                prevprobnow = prevprob * self.infosets.Actions_Prob[idxcurnode][idslist] * self.infosets.Nature_Weight[idxcurnode][idslist][idson]
                            if self.infosets.Player[dson] == selectplayer :
                                self.infosets.OppoProbability[dson] += prevprobnow
                            recursive_probs_oppo_abstract(dson,prevprobnow)
                            
        selectplayer = 1
        recursive_probs_oppo_abstract(startingnodeidx, prevprob = self.infosets.OppoProbability[startingnodeidx])
        selectplayer = 2 
        recursive_probs_oppo_abstract(startingnodeidx, prevprob = self.infosets.OppoProbability[startingnodeidx])
    
'''
    def recursive_utility_call(self,startingabsidx, init = False, oppo_prob = True):

        if init:
            self.infosets.Exp_Utility = [0.0 for _ in range(len(self.infosets.index))]

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

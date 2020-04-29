import numpy as np
from Gamer import *

class Vanilla_Gamer(Gamer):

    def __init__(self, infosets, nodes) :
        super().__init__(infosets, nodes)
        self.utilities   = [[] for _ in range(len(self.infosets.index))]
        self.cfutilities = [[] for _ in range(len(self.infosets.index))]


################################################################################
    def tree_drop(self) : ## Top-Bottom of the tree
        roots = self.infosets.index[self.infosets.Depth == 1]
        for startingidx in roots:
            self.infosets.Probability[startingidx] = 1
            self.infosets.Probability_Opp[startingidx] = 1
            self.recursive_probs(startingidx)
            self.recursive_probs_oppo(startingidx, "1", initialize = True)
            self.recursive_probs_oppo(startingidx, "2")
###############################################################################

    def recursive_probs(self, idxcur) :
        if self.infosets.Direct_Sons[idxcur] != -1 :
            for idson in range(len(self.infosets.Direct_Sons[idxcur])) :
                dson = self.infosets.Direct_Sons[idxcur][idson]
                self.infosets.Probability[dson] = self.infosets.Probability[idxcur] * self.strategies[idxcur][idson]
                self.recursive_probs(dson)

    def recursive_probs_oppo(self,startingnodeidx,player,initialize = False):

        # Probabilities given by the opponents are initialized and will begin at startingnodeidx
        if initialize :
            self.nodes.Probability_Opp = [0.0 for _ in range(len(self.nodes['Probability']))]
            self.nodes.Probability_Opp[startingnodeidx] = 1

        # Recursive function to update the probabilities given by the opponent starting from startingnodeidx and going down
        def recursive_probs_oppo_query(idxcurnode,prevprob) :
            if self.nodes.Direct_Sons[idxcurnode] != -1 : # Not a leaf
                for idson in range(len(self.nodes.Direct_Sons[idxcurnode])) : # Cycles the direct sons
                    dson = self.nodes.Direct_Sons[idxcurnode][idson]
                    prevprobnow = prevprob
                    if self.nodes.Player[idxcurnode] != player : # If it's an opponent node, keeps track of probabilities
                        prevprobnow = prevprobnow * self.nodes.Actions_Prob[idxcurnode][idson]
                    if self.nodes.Player[dson] == player : # Updates the df of the son
                        self.nodes.Probability_Opp[dson] = prevprobnow
                    recursive_probs_oppo_query(dson, prevprobnow) # The recursion goes on anyways

        # Calls the recursive function for probabilities
        recursive_probs_oppo_query(startingnodeidx,self.nodes.Probability_Opp[startingnodeidx])

    # Infosets probabilities
    def recursive_probs_abstract_call(self, startingnodeidx, prevprob = 1, init = False) :

        if init :
            self.infosets.Probability =[0.0 for _ in range(len(self.infosets.index))]
            self.nodes.Probability[startingnodeidx] = 1

        def recursive_probs_abstract(idxcurnode, prevprob = 1) :
            dslists = self.infosets.Direct_Sons[idxcurnode]
            for idslist in range(len(dslists)) : # select one action
                print(idslist)
                if len(dslists) > 0 :
                    print(dslists)
                    print(idslist)
                    dslist = dslists[idslist]
                    if len(dslist) > 0 :
                        for idson in range(len(dslist)) : # select one infoset
                            dson = dslist[idson]
                            print(dson)
                            prevprobnow = prevprob * self.infosets.Actions_Prob[idxcurnode][idslist] * self.infosets.Nature_Weight[idxcurnode][idslist][idson]
                            self.infosets.Probability[dson] += prevprobnow
                            recursive_probs_abstract(dson,prevprobnow)

        recursive_probs_abstract(startingnodeidx, prevprob = 1)

################################################################################
'''
    def get_payoff(self, idxcurnode, action = None):
        ds = self.nodes.Direct_Sons[idxcurnode][action]
        def recursive_payoff(self,idxcurnode):
            if self.nodes.Direct_Sons[idxcurnode] != -1 :
                for idson in range(len(self.nodes.Direct_Sons[idxcurnode])) :
                    dson = self.nodes.Direct_Sons[idxcurnode][idson]
                    self.nodes.Probability[dson] = self.nodes.Probability[idxcurnode] * self.nodes.Actions_Prob[idxcurnode][idson]
                    self.recursive_probs(dson)
            else:

        recursive_payoff(ds)


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

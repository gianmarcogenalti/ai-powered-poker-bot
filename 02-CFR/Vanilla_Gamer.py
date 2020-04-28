import numpy as np
from Gamer import *

class Vanilla_Gamer(Gamer):

    def __init__(self, infosets, nodes) :
        super().__init__(infosets, nodes)
        self.utilities   = [[] for _ in range(len(self.infosets.index))]
        self.cfutilities = [[] for _ in range(len(self.infosets.index))]

################################################################################
    def tree_drop(self) : ## Top-Bottom of the tree
        startingnodeidx = self.nodes.index[self.nodes.Depth == 0][0]
        self.nodes['Probability'][startingnodeidx] = 1
        self.recursive_probs(startingnodeidx)
        self.recursive_probs_oppo(startingnodeidx, 1)


    def recursive_probs(self, idxcurnode) :
        if self.nodes.Direct_Sons[idxcurnode] != -1 :
            for idson in range(len(self.nodes.Direct_Sons[idxcurnode])) :
                dson = self.nodes.Direct_Sons[idxcurnode][idson]
                self.nodes.Probability[dson] = self.nodes.Probability[idxcurnode] * self.nodes.Actions_Prob[idxcurnode][idson]
                self.recursive_probs(dson)

    def recursive_probs_oppo(self,idxcurnode,player):
        prevprob = np.ones(len(self.nodes.index))
        def recursive_query(idxcurnode) :
            if self.nodes.Direct_Sons[idxcurnode] != -1 :
                for idson in range(len(self.nodes.Direct_Sons[idxcurnode])) :
                    dson = self.nodes.Direct_Sons[idxcurnode][idson]
                    if self.nodes.Player[dson] != player :
                        self.nodes.Probability_Opp[dson] = prevprob[idxcurnode]
                    else :
                        prevprob[dson] = prevprob[dson] * self.nodes.Actions_Prob[idxcurnode][idson]
                    recursive_query(dson)
        recursive_query(idxcurnode)
        self.nodes['Probability_Opp'] = prevprob

    def recursive_payoff(self,idxcurnode):
        utility = 0.
        if self.nodes.Type[idxcurnode] == 'L':
            print(self.nodes.Payoff_Vector_P1[0])
            return self.nodes.Payoff_Vector_P1[0]
        for ds in range(len(self.nodes.Direct_Sons[idxcurnode])):
            utility += self.recursive_payoff(self.nodes.Direct_Sons[idxcurnode][ds])*self.nodes.Actions_Prob[idxcurnode][ds]
        return utility
'''
    def get_payoff(self, idxcurnode, action = None):
        ds = self.nodes.Direct_Sons[idxcurnode][action]
        def recursive_payoff(self,idxcurnode):


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

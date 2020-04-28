from Gamer import *

class Vanilla_Gamer(Gamer):
    def __init__(self, infosets, nodes) :
        super().__init__(infosets, nodes)
        self.utilities   = [[] for _ in range(len(self.infosets.index))]
        self.cfutilities = [[] for _ in range(len(self.infosets.index))]
################################################################################
'''
HERE WE NEED TO IMPLEMENTE THE COLUMN 'Opp_Probability'
'''
    def recursive_probs(self, idxcurnode):
        if self.nodes.Direct_Sons[idxcurnode] != -1 :
            for idson in range(len(self.nodes.Direct_Sons[idxcurnode])) :
                dson = self.nodes.Direct_Sons[idxcurnode][idson]
                self.nodes.Probability[dson] = self.nodes.Probability[idxcurnode] * self.nodes.Actions_Prob[idxcurnode][idson]
                self.recursive_probs(dson)
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
    def tree_drop(self) : ## Top-Bottom of the tree
        startingnodeidx = self.nodes.index[self.nodes.Depth == 0][0]
        self.nodes['Probability'][startingnodeidx] = 1
        self.recursive_probs(startingnodeidx)
################################################################################
    def update_abstract(self, abs_index, regrets):
        for i in self.infosets.Index_Members[abs_index]:
            self.nodes.Actions_Prob[i] = new_strat
            self.recursive_probs(i)
            utility = 0.
            for son in self.nodes.Sons[i]:
                if self.nodes.Type[son] == 'L':
                    utility += self.nodes.Payoff_Vector_P1[son]*self.nodes.Probability[son]
            self.nodes.Exp_Utility[i] = utility
################################################################################
    def abs_regrets(self, abs_index):

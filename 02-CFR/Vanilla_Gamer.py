from Gamer import *

class Vanilla_Gamer(Gamer):
    def __init__(self, infosets, nodes) :
        super().__init__(infosets, nodes)
################################################################################
    def tree_drop(self) : ## Top-Bottom of the tree
        startingnodeidx = self.nodes.index[self.nodes.Depth == 0][0]

        def recursive_probs(idxcurnode) :
            if self.nodes.Direct_Sons[idxcurnode] != -1 :
                for idson in range(len(self.nodes.Direct_Sons[idxcurnode])) :
                    dson = self.nodes.Direct_Sons[idxcurnode][idson]
                    self.nodes.Probability[dson] = self.nodes.Probability[idxcurnode] * self.nodes.Actions_Prob[idxcurnode][idson]
                    recursive_probs(dson)

        self.nodes['Probability'][startingnodeidx] = 1
        recursive_probs(startingnodeidx)
################################################################################
    def tree_climb(self):
        print("monkey!")
################################################################################
    def 

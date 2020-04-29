import numpy as np

def init_probabilities(infosets):
    probabilities = [[] for _ in range(len(infosets.index))]
    regrets = [[] for _ in range(len(infosets.index))]
    for index,row in infosets.iterrows():
        n_actions = len(row.Actions)
        regrets[index] = np.zeros(n_actions)
        for pr_act in range(n_actions):
            probabilities[index].append(1/n_actions)
    infosets['Actions_Prob'] = probabilities
    return probabilities, regrets

class Gamer() :
    def __init__(self, infosets, nodes) :
        self.infosets = infosets
        self.nodes = nodes
        self.t = 0
        self.strategies = init_probabilities(self.infosets)[0]
        self.cumulative_regret = init_probabilities(self.infosets)[1] ##PLUS

    def regret_matching(self, info_index) :
        new_strats = []
        sum_regret = sum(self.cumulative_regret[info_index])
        n_actions = len(self.cumulative_regret[info_index])
        if sum_regret == 0:
            self.strategies[info_index] = np.repeat(1/n_actions, n_actions)
        else:
            for i in range(n_actions):
                new_strats.append(self.cumulative_regret[info_index][i]/sum_regret)

        return new_strats


    def update_strategies(self, info_index, regrets) :

        for act in range(len(self.cumulative_regret[info_index])):
            self.cumulative_regret[info_index][act] = max(self.cumulative_regret[info_index][act] + regrets[act], 0)

        self.strategies[info_index] = self.regret_matching(info_index)

        for m in infosets.Index_Members[info_index]:
            self.nodes.Actions_Prob[m] = self.strategies[info_index]

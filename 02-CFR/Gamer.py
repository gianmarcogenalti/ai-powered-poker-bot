import numpy as np

def init_probabilities(infosets):
    probabilities = [[] for _ in range(len(infosets.index))]
    regrets = [[] for _ in range(len(infosets.index))]
    for index,row in infosets.iterrows():
        n_actions = len(row.Actions)
        regrets[index] = np.zeros(n_actions)
        for pr_act in range(n_actions):
            probabilities[index].append(1/n_actions)

    return probabilities, regrets

class Gamer() :
    def __init__(self, infosets, nodes) :
        self.infosets = infosets
        self.nodes = nodes
        self.t = 0
        self.strategies = init_probabilities(infosets)[0]
        self.cumulative_regret = init_probabilities(infosets)[1]


    def update_strategies(self, info_index, action_index, new_strategies, regret) :
        self.strategies[info_index] = new_strategies
        self.cumulative_regret[info_index][action_index] += regret

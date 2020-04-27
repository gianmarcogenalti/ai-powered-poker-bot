def init_probabilities(infosets):
    probabilities = [[] for _ in range(len(infosets.index))]
    for index,row in infosets.iterrows():
        n_actions = len(row.Actions)
        for pr_act in range(n_actions):
            probabilities[index].append(1/n_actions)

    return probabilities

class Gamer() :
    def __init__(self, infosets) :
        self.game = infosets
        self.t = 0
        self.strategies = init_probabilities(infosets)
        self.cumulative_regret = 0


    def update_strategies(self, info_index, new_strategies, regret) :
        self.strategies[info_index] = new_strategies
        self.cumulative_regret += regret

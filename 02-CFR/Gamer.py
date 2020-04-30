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
            for i in range(n_actions - 1):
                self.strategies[info_index][i] = 1/n_actions
            self.strategies[info_index][n_actions -1] = 1 - sum(self.strategies[info_index][:(n_actions-1)])
        else:
            for i in range(n_actions):
                self.strategies[info_index][i] = self.cumulative_regret[info_index][i]/sum_regret

    def update_strategies(self, info_index, regrets) :

        for act in range(len(self.cumulative_regret[info_index])):
            self.cumulative_regret[info_index][act] = max(self.cumulative_regret[info_index][act] + regrets[act], 0)
        self.regret_matching(info_index)


    def print_output(self, game, true_infosets) :
        filename = "output - " + game + ".txt"
        file1 = open(filename,"w")
        for index, row in true_infosets.iterrows():
            line = "infoset " + row.History + " strategies"
            clust = row.Map_Clust[0]
            for action in range(len(row.Actions)):
                line += " " + row.Actions[action] + "=" + str(self.strategies[clust][action])
            file1.write(line + "\n")

        file1.close()

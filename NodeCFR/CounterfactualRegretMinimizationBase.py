import random

class CounterfactualRegretMinimizationBase:
    def __init__(self, nodes, chance_sampling = False):
        self.root               = nodes.index[-1]
        self.nodes              = nodes
        self.sigma              = self.init_sigma(self.root)
        self.cumulative_regrets = self.init_empty_node_maps(self.root)
        self.cumulative_sigma   = self.init_empty_node_maps(self.root)
        self.nash_equilibrium   = self.init_empty_node_maps(self.root)
        self.chance_sampling    = chance_sampling

################################################################################
## updates strategies
    def _update_sigma(self, node):
        if self.nodes.Type[node] =='N':
            abs_index = self.nodes.Abs_Map[node]
            rgrt_sum = sum(filter(lambda x : x > 0, self.cumulative_regrets[abs_index].values()))
            for a in self.cumulative_regrets[abs_index]:
                self.sigma[abs_index][a] = max(self.cumulative_regrets[abs_index][a], 0.) / rgrt_sum if rgrt_sum > 0 else 1. / len(self.cumulative_regrets[abs_index].keys())

################################################################################
## Computation of nash equilibrium, to launch at the end
    def compute_nash_equilibrium(self):
        #print(self.cumulative_sigma)
        self.__compute_ne_rec(self.root)

    def __compute_ne_rec(self, node):
        if self.nodes.Type[node] == "L":
            return
        abs_index = self.nodes.Abs_Map[node]
        if self.nodes.Type[node] == "C": ### i nodi della nature sono considerati infoset e il loro equilibrio di nash sono le probabilità delle mosse
            self.nash_equilibrium[abs_index] = self.sigma[abs_index]#{self.nodes.Actions[node][idaction]: self.nodes.Actions_Prob[node][idaction] for idaction in range(len(self.nodes.Actions[node]))}
        else:
            sigma_sum = sum(self.cumulative_sigma[abs_index].values())
            #print(abs_index,self.cumulative_sigma[abs_index])
            #print(node)
            self.nash_equilibrium[abs_index] = {a: self.cumulative_sigma[abs_index][a] / sigma_sum for a in self.nodes.Actions[node]}
        # go to subtrees
        #print(self.nash_equilibrium[abs_index])
        for k in self.nodes.Direct_Sons[node]:
            self.__compute_ne_rec(k)
################################################################################
## some updates
    def _cumulate_cfr_regret(self, node, idaction, regret):
        information_set = self.nodes.Abs_Map[node]
        action = self.nodes.Actions[node][idaction]
        self.cumulative_regrets[information_set][action] += regret

    def _cumulate_sigma(self, node, idaction, prob):
        information_set = self.nodes.Abs_Map[node]
        action = self.nodes.Actions[node][idaction]
        self.cumulative_sigma[information_set][action] += prob
################################################################################
## virtual function
    def run(self, iterations):
        raise NotImplementedError("Please implement run method")
################################################################################
## per ogni nodo calcola la somma dei payoff pesata sulla probabilità di arrivarci
    def value_of_the_game(self):
        return self.__value_of_the_game_state_recursive(self.root)

    def __value_of_the_game_state_recursive(self, node):
        value = 0.
        if self.nodes.Type[node] == "L":
            return self.nodes.Payoff_Vector_P1[node][0]
        for idaction in range(len(self.nodes.Actions[node])):
            value +=  self.nash_equilibrium[self.nodes.Abs_Map[node]][idaction] * self.__value_of_the_game_state_recursive(self.nodes.Direct_Sons[node][idaction])
        return value
################################################################################
    def _cfr_utility_recursive(self, node, reach_a, reach_b):
        children_states_utilities = {}
        if self.nodes.Type[node]=="L":
            return self.nodes.Payoff_Vector_P1[node][0]
        if self.nodes.Type[node]=="C":
            if self.chance_sampling:
                dslist = self.nodes.Direct_Sons[node]
                random_ds = random.choice(dslist)
                return self._cfr_utility_recursive(random_ds, reach_a, reach_b)
            else:
                sm = 0
                counter = 0
                for outcome in self.nodes.Direct_Sons[node]:
                    sm += self.nodes.Actions_Prob[node][counter]*self._cfr_utility_recursive(outcome, reach_a, reach_b)
                    counter += 1
                return sm
        value = 0.
        for idaction,action in enumerate(self.nodes.Actions[node]):
            child_reach_a = reach_a * (self.sigma[self.nodes.Abs_Map[node]][action] if self.nodes.Player[node] == 1 else 1)
            child_reach_b = reach_b * (self.sigma[self.nodes.Abs_Map[node]][action] if self.nodes.Player[node] == 2 else 1)
            child_state_utility = self._cfr_utility_recursive(self.nodes.Direct_Sons[node][idaction], child_reach_a, child_reach_b)
            action = self.nodes.Actions[node][idaction]
            value +=  self.sigma[self.nodes.Abs_Map[node]][action] * child_state_utility
            children_states_utilities[idaction] = child_state_utility

        (cfr_reach, reach) = (reach_b, reach_a) if self.nodes.Player[node] == 1 else (reach_a, reach_b)

        for idaction in range(len(self.nodes.Actions[node])):
            action = self.nodes.Actions[node][idaction]
            if self.nodes.Player[node] == 2:
                sign = -1
            else:
                sign = 1
            action_cfr_regret = sign * cfr_reach * (children_states_utilities[idaction] - value)
            self._cumulate_cfr_regret(node, idaction, action_cfr_regret)
            self._cumulate_sigma(node, idaction, reach * self.sigma[self.nodes.Abs_Map[node]][action])
        if self.chance_sampling:
            self._update_sigma(node)
        return value
################################################################################
    def init_sigma(self, node, output = None):
        output = dict()
        def init_sigma_recursive(node):
            if self.nodes.Type[node] == 'L':
                return
            if self.nodes.Type[node] == 'C':
                output[self.nodes.Abs_Map[node]] = {self.nodes.Actions[node][idaction]: self.nodes.Actions_Prob[node][idaction] for idaction in range(len(self.nodes.Actions[node]))}
            else:
                output[self.nodes.Abs_Map[node]] = {action: 1. / len(self.nodes.Actions[node]) for action in self.nodes.Actions[node]}
            for ds in self.nodes.Direct_Sons[node]:
                init_sigma_recursive(ds)
        init_sigma_recursive(node)
        #print(output)
        return output

    def init_empty_node_maps(self, node, output = None):
        output = dict()
        def init_empty_node_maps_recursive(node):
            if self.nodes.Type[node] == 'L':
                return
            output[self.nodes.Abs_Map[node]] = {action: 0. for action in self.nodes.Actions[node]}
            for ds in self.nodes.Direct_Sons[node]:
                init_empty_node_maps_recursive(ds)
        init_empty_node_maps_recursive(node)
        #print(output)
        return output
################################################################################
## output printing

    def print_output(self, game, method, true_infosets) :
        filename = method + "_nash_output - " + game + ".txt"
        filename2 = method + "_sigma_output - " + game + ".txt"
        file1 = open(filename,"a")
        file1.truncate(0)
        file2 = open(filename2, "a")
        file2.truncate(0)
        for index, row in true_infosets.iterrows():
            line = "infoset " + row.History + " nash_equilibriums"
            line2 = "infoset " + row.History + " strategies"
            clust = row.Map_Clust[0]
            for idaction in range(len(row.Actions)):
                action = row.Actions[idaction]
                line += " " + row.Actions[idaction] + "=" + str(self.nash_equilibrium[clust][action])
                line2 += " " + row.Actions[idaction] + "=" + str(self.sigma[clust][action])
            file1.write(line + "\n")
            file2.write(line2 + "\n")

        file1.close()

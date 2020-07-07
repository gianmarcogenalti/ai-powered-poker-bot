import random

class CounterfactualRegretMinimizationBase:
    def __init__(self, nodes, abs_infosets, roots, leaves, players, it, chance_sampling = False):
        self.it                 = it
        self.subgameplayer      = players[it]
        if self.subgameplayer == 2:
            self.opponent       = 1
        if self.subgameplayer == 1:
            self.opponent       = 2
        self.root               = nodes.index[-(len(roots)-it)]
        print(self.root)
        self.nodes              = nodes
        self.info_roots         = roots[it]
        self.info_leaves        = leaves[it]
        self.sigma              = self.init_sigma(self.root, abs_infosets)
        self.cumulative_regrets = self.init_empty_node_maps(self.root, abs_infosets)
        self.cumulative_sigma   = self.init_empty_node_maps(self.root, abs_infosets)
        self.nash_equilibrium   = self.init_empty_node_maps(self.root, abs_infosets)
        self.chance_sampling    = chance_sampling
################################################################################
    def return_ne_ec(self):
        '''
        ret = [self.nash_equilibrium[i] for i in self.info_roots]
        return ret
        '''
        return self.nash_equilibrium
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
        self.__compute_ne_rec(self.root)

    def __compute_ne_rec(self, node):
        if self.nodes.Dad[node] != 999999:
            grandpa = self.nodes.Dad[self.nodes.Dad[node]]
            if grandpa != -1:
                if self.nodes.Type[node] == "L" or self.nodes.Abs_Map[self.nodes.Dad[node]] in self.info_leaves or self.nodes.Abs_Map[grandpa] in self.info_leaves :
                    return
        abs_index = self.nodes.Abs_Map[node]
        if self.nodes.Type[node] == "C": ### i nodi della nature sono considerati infoset e il loro equilibrio di nash sono le probabilità delle mosse
            self.nash_equilibrium[abs_index] = {self.nodes.Actions[node][idaction]: self.nodes.Actions_Prob[node][idaction] for idaction in range(len(self.nodes.Actions[node]))}
        else:
            sigma_sum = sum(self.cumulative_sigma[abs_index].values())
        if self.nodes.Player[node] == self.opponent or self.nodes.Abs_Map[node] in self.info_roots:
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
        raise NotImplementedError("No method specified")
################################################################################
## per ogni nodo calcola la somma dei payoff pesata sulla probabilità di arrivarci
    def value_of_the_game(self):
        return self.__value_of_the_game_state_recursive(self.root)

    def __value_of_the_game_state_recursive(self, node):
        value = 0.
        if self.nodes.Dad[node] != 999999:
            grandpa = self.nodes.Dad[self.nodes.Dad[node]]
            if grandpa != -1:
                if self.nodes.Type[node] == "L" or self.nodes.Abs_Map[self.nodes.Dad[node]] in self.info_leaves or self.nodes.Abs_Map[grandpa] in self.info_leaves :
                    return self.nodes.Expected_Payoff[node]
        for idaction in range(len(self.nodes.Actions[node])):
            value +=  self.nash_equilibrium[self.nodes.Abs_Map[node]][idaction] * self.__value_of_the_game_state_recursive(self.nodes.Direct_Sons[node][idaction])
        return value
################################################################################
    def _cfr_utility_recursive(self, node, reach_a, reach_b):
        children_states_utilities = {}
        if self.nodes.Dad[node] != 999999:
            grandpa = self.nodes.Dad[self.nodes.Dad[node]]
            if grandpa != -1:
                if self.nodes.Type[node]=="L" or self.nodes.Abs_Map[self.nodes.Dad[node]] in self.info_leaves or self.nodes.Abs_Map[grandpa] in self.info_leaves :
                    # evaluate terminal node according to the game result
                    return self.nodes.Expected_Payoff[node]
        if self.nodes.Type[node]=="C":
            if self.chance_sampling:
                # if node is a chance node, lets sample one child node and proceed normally
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
        # sum up all utilities for playing actions in our game state
        value = 0.
        for idaction in range(len(self.nodes.Actions[node])):
            action = self.nodes.Actions[node][idaction]
            child_reach_a = reach_a * (self.sigma[self.nodes.Abs_Map[node]][action] if self.nodes.Player[node] == 1 else 1)
            child_reach_b = reach_b * (self.sigma[self.nodes.Abs_Map[node]][action] if self.nodes.Player[node] == 2 else 1)
            # value as if child state implied by chosen action was a game tree root
            child_state_utility = self._cfr_utility_recursive(self.nodes.Direct_Sons[node][idaction], child_reach_a, child_reach_b)
            # value computation for current node
            value +=  self.sigma[self.nodes.Abs_Map[node]][action] * child_state_utility
            # values for chosen actions (child nodes) are kept here
            children_states_utilities[idaction] = child_state_utility

        # we are computing regrets for both players simultaneously, therefore we need to relate reach,reach_opponent to the player acting
        # in current node, for player A, it is different than for player B
        (cfr_reach, reach) = (reach_b, reach_a) if self.nodes.Player[node] == 1 else (reach_a, reach_b)
        if self.nodes.Player[node] == self.opponent or self.nodes.Abs_Map[node] in self.info_roots:
            for idaction in range(len(self.nodes.Actions[node])):
                action = self.nodes.Actions[node][idaction]
                # we multiply regret by -1 for player B, this is because value is computed from player A perspective
                # again we need that perspective switch
                if self.nodes.Player[node] == 2:
                    sign = -1
                else:
                    sign = 1
                action_cfr_regret = sign * cfr_reach * (children_states_utilities[idaction] - value)
                self._cumulate_cfr_regret(node, idaction, action_cfr_regret)
                self._cumulate_sigma(node, idaction, reach * self.sigma[self.nodes.Abs_Map[node]][action])
            if self.chance_sampling:
                # update sigma according to cumulative regrets - we can do it here because we are using chance sampling
                # and so we only visit single game_state from an information set (chance is sampled once)
                self._update_sigma(node)
        return value
################################################################################

    def init_sigma(self,node, abs_infosets, output = None):
        output = dict()
        for index, row in abs_infosets[abs_infosets.Dads != 999999].iterrows():
            output[index] = {row.Actions[idaction]: row.Actions_Prob[idaction] for idaction in range(len(row.Actions))}
        #print(output)
        return output

    def init_empty_node_maps(self,node, abs_infosets, output = None):
        output = dict()
        for index, row in abs_infosets[abs_infosets.Dads != 999999].iterrows():
            output[index] = {row.Actions[idaction]: 0 for idaction in range(len(row.Actions))}
        return output



class CounterfactualRegretMinimizationBase:
    def __init__(self, chance_sampling = False, nodes, abs_infosets):
        self.root               = nodes.index[-1]
        self.sigma              = init_sigma(root)
        self.cumulative_regrets = init_empty_node_maps(root)
        self.cumulative_sigma   = init_empty_node_maps(root)
        self.nash_equilibrium   = init_empty_node_maps(root)
        self.chance_sampling    = chance_sampling
        self.nodes              = nodes

    def _update_sigma(self, i):
        rgrt_sum = sum(filter(lambda x : x > 0, self.cumulative_regrets[i].values()))
        for a in self.cumulative_regrets[i]:
            self.sigma[i][a] = max(self.cumulative_regrets[i][a], 0.) / rgrt_sum if rgrt_sum > 0 else 1. / len(self.cumulative_regrets[i].keys())


    def compute_nash_equilibrium(self):
        self.__compute_ne_rec(self.root)


    def __compute_ne_rec(self, node):
        if self.nodes.Type[node]=="L":
            return
        i = self.nodes.Map[node]
        if self.nodes.Type[node]=="C":
            self.nash_equilibrium[i] = {a:node.chance_prob() for a in node.actions}
        else:
            sigma_sum = sum(self.cumulative_sigma[i].values())
            self.nash_equilibrium[i] = {a: self.cumulative_sigma[i][a] / sigma_sum for a in node.actions}
        # go to subtrees
        for k in self.nodes.Direct_Sons[node]:
            self.__compute_ne_rec(k)

    def _cumulate_cfr_regret(self, information_set, action, regret):
        self.cumulative_regrets[information_set][action] += regret


    def _cumulate_sigma(self, information_set, action, prob):
        self.cumulative_sigma[information_set][action] += prob


    def run(self, iterations):
        raise NotImplementedError("Please implement run method")



    def value_of_the_game(self):
        return self.__value_of_the_game_state_recursive(self.root)



    def _cfr_utility_recursive(self, state, reach_a, reach_b):
        children_states_utilities = {}
        if self.nodes.Type[node]=="L":
            # evaluate terminal node according to the game result
            return self.nodes.Payoff_P1[node]
        if self.nodes.Type[node]=="C":
            if self.chance_sampling:
                # if node is a chance node, lets sample one child node and proceed normally
                return self._cfr_utility_recursive(state.sample_one(), reach_a, reach_b)
            else:
                chance_outcomes = {self.nodes.index[ds] for ds in self.nodes.Direct_Sons[node]}
                return self.nodes.Actions_Prob[node]* sum([self._cfr_utility_recursive(outcome, reach_a, reach_b) for outcome in chance_outcomes])
        # sum up all utilities for playing actions in our game state
        value = 0.
        for idaction in range(len(self.nodes.Actions[node])):
            child_reach_a = reach_a * (self.sigma[self.nodes.Map[node]][idaction] if self.nodes.Player[node] == 1 else 1)
            child_reach_a = reach_a * (self.sigma[self.nodes.Map[node]][idaction] if self.nodes.Player[node] == 2 else 1)
            # value as if child state implied by chosen action was a game tree root
            child_state_utility = self._cfr_utility_recursive(self.nodes.Direct_Sons[node][idaction], child_reach_a, child_reach_b)
            # value computation for current node
            value +=  self.sigma[self.nodes.Map[node]][idaction] * child_state_utility
            # values for chosen actions (child nodes) are kept here
            children_states_utilities[idaction] = child_state_utility

        # we are computing regrets for both players simultaneously, therefore we need to relate reach,reach_opponent to the player acting
        # in current node, for player A, it is different than for player B
        (cfr_reach, reach) = (reach_b, reach_a) if self.nodes.Player[node] == 1 else (reach_a, reach_b)

        for idaction in range(len(self.nodes.Actions[node])):
            # we multiply regret by -1 for player B, this is because value is computed from player A perspective
            # again we need that perspective switch
            action_cfr_regret = self.Player[node] * cfr_reach * (children_states_utilities[idaction] - value)
            self._cumulate_cfr_regret(self.nodes.Map[node], idaction, action_cfr_regret)
            self._cumulate_sigma(self.nodes.Map[node], idaction, reach * self.sigma[self.nodes.Map[node]][idaction])
        if self.chance_sampling:
            # update sigma according to cumulative regrets - we can do it here because we are using chance sampling
            # and so we only visit single game_state from an information set (chance is sampled once)
            self._update_sigma(self.nodes.Map[node])
        return value



    def __value_of_the_game_state_recursive(self, node):
        value = 0.
        if self.nodes.Type[node]=="L":
            return   self.nodes.Payoff_P1[node]
        for idaction in range(len(self.nodes.Actions[node])):
            value +=  self.nash_equilibrium[self.nodes.Map[node]][idaction] * self.__value_of_the_game_state_recursive(self.nodes.Direct_Sons[node][idaction])
        return value



<<<<<<< HEAD

    def __value_of_the_game_state_recursive(self, node):
        value = 0.
        if node.is_terminal():
            return node.evaluation()
        for action in node.actions:
            value +=  self.nash_equilibrium[node.inf_set()][action] * self.__value_of_the_game_state_recursive(node.play(action))
        return value
=======
>>>>>>> 14076f81137543af7c6236dee3a7b89282127e9a

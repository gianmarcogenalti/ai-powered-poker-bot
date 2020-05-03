import numpy as np
from Gamer import *
import time
import numpy as np
import math
'''
def init_n_actions(strategies):
    ret = 0
    for i in strategies:
        ret += len(i)
    return ret
'''
class MC_Gamer(Gamer):

    def __init__(self, infosets, nodes) :
        super().__init__(infosets, nodes)
        self.utilities   = np.zeros(len(self.infosets.index))
        self.cfutilities = [[] for _ in range(len(self.infosets.index))]
        self.root = -1
        #self.Probability_Opp = [0.0 for _ in range(len(self.infosets.index))]
        #self.Probability_P1 = [0.0 for _ in range(len(self.infosets.index))]
        #self.Probability_P2 = [0.0 for _ in range(len(self.infosets.index))]
        #self.cumpayoff = [0.0 for _ in range(len(self.infosets.index))]
        #self.n_actions = init_n_actions(self.strategies)
        self.proxy = [np.zeros(len(self.strategies[_])) for _ in range(len(self.strategies))]
################################################################################
    def train(self, T):
        t0 = time.time()
        while self.t < T:
                self.waterlilies_select(1)
                print("The first frog selected the waterlilies!")
                self.waterlilies_jumps(2)
                print("The second frog jumped on the waterlilies!")
                self.waterlilies_select(2)
                print("The second frog selected other waterlilies!")
                self.waterlilies_jumps(1)
                print("The first frog jumped on the other waterlilies!")
                self.t += 1
                print("The frogs had %d challenges!" % self.t)
        print("After %d challenges the frogs got bored!" % (time.time() - t0))

################################################################################
    def get_regrets(self, absidx):
        regrets = []
        for act in range(len(self.infosets.Actions[absidx])):
            regrets.append(self.cfutilities[absidx][act] - self.utilities[absidx])
        return regrets

################################################################################
    def waterlilies_select(self, opponent):
        self.root = int(np.random.choice(range(len(self.infosets.index[self.infosets.Depth == 1]))))
        self.proxy = [np.zeros(len(self.strategies[_])) for _ in range(len(self.strategies))]
        opp_indices = self.infosets.index[self.infosets.Player == opponent]
        for idx in opp_indices:
            act_index = int(np.random.choice(range(len(self.strategies[idx])), 1))
            self.proxy[idx][act_index] = self.strategies[idx][act_index]

            indices = self.infosets.index[self.infosets.Player != opponent]
            for i in indices:
                self.proxy[i] = self.strategies[i]
################################################################################

    def waterlilies_jumps(self, player):
        sign = 1 if player == 1 else -1
        #payoff = [0.0 for _ in range(len(self.infosets.index))]
        terminals = []
        dads = [[] for _ in range(len(self.infosets.index))]
        dad_probs = [[] for _ in range(len(self.infosets.index))]
        dad_actions = [[] for _ in range(len(self.infosets.index))]
        player_depths = self.infosets.Depth[self.infosets.Player == player]
        for depth in range(1,max(self.infosets['Depth']) + 1):
            if depth == 1:
                icurinfosets = [self.root]
            else:
                icurinfosets = list(self.infosets.index[self.infosets['Depth'] == depth])
            for icurinfo in icurinfosets :
                print(icurinfo)
                dslists = self.infosets.Direct_Sons[icurinfo]
                for idslist in range(len(dslists)) : # select one action
                    dslist = dslists[idslist]
                    if self.proxy[icurinfo][idslist] > 0.0:
                        if len(dslist) == 0:
                            self.utilities[icurinfo] += self.infosets.Payoff_P1[icurinfo][idslist] * self.proxy[icurinfo][idslist] * sign
                            self.cfutilities[icurinfo].append(self.infosets.Payoff_P1[icurinfo][idslist] * sign)
                            if (icurinfo not in terminals) and depth in player_depths:
                                terminals.append(icurinfo)
                            for d in range(len(dads[icurinfo])):
                                print(d)
                                print(dad_actions[icurinfo][d])
                                self.utilities[dads[icurinfo][d]] += dad_probs[icurinfo][d] * self.utilities[icurinfo] * sign
                                self.cfutilities[dads[icurinfo][d]][dad_actions[icurinfo][d]] += self.utilities[icurinfo]*sign
                        else:
                            self.cfutilities[icurinfo].append(0)
                            for idson in range(len(dslist)) : # select one son infoset
                                dson = dslist[idson]
                                '''
                                if self.infosets.Player[icurinfo] == 1 :
                                    self.Probability_P1[dson] += self.Probability_P1[icurinfo] * self.strategies[icurinfo][idslist] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                                    self.Probability_P2[dson] += self.Probability_P2[icurinfo] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                                else :
                                    self.Probability_P2[dson] += self.Probability_P2[icurinfo] * self.strategies[icurinfo][idslist] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                                    self.Probability_P1[dson] += self.Probability_P1[icurinfo] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                                if self.infosets.Player[dson] == 1 :
                                    self.Probability_Opp[dson] = self.Probability_P2[dson]
                                else :
                                    self.Probability_Opp[dson] = self.Probability_P1[dson]
                                '''
                                dads[dson].append(icurinfo)
                                dad_probs[dson].append(self.proxy[icurinfo][idslist]*self.infosets.Nature_Weight[icurinfo][idslist][idson])
                                dad_actions[dson].append(idslist)

        for t in terminals:
            regrets = get_regrets(t, payoff)
            update_strategies(t, regrets)
################################################################################

    def tree_climb(self, player) :
        self.utilities   = np.zeros(len(self.infosets.index))
        self.cfutilities = [[] for _ in range(len(self.infosets.index))]
        #payoffsums = [0.0 for _ in range(len(self.infosets.index))]
        sign = 1 if player == 1 else -1
        #dpt_player = self.infosets.Depth[self.infosets.Player == player]
        for dpt in reversed(range(1, max(self.infosets.Depth) + 1)):
            if dpt == 1:
                dpt_indices = [self.root]
            else:
                dpt_indices = self.infosets.index[self.infosets.Depth == dpt]
            for index in dpt_indices:
                    self.utilities[index] = 0.0
                    for idlist in range(len(self.infosets.Direct_Sons[index])):
                        dslist = self.infosets.Direct_Sons[index][idlist]
                        if len(dslist) == 0:
                            payoffsums[index] += self.infosets.Payoff_P1[index][idlist] * self.strategies[index][idlist]
                            #self.utilities[index] += self.Probability_Opp[index]*self.strategies[index][idlist]*sign*self.infosets.Payoff_P1[index][idlist]
                            if iteration:
                                self.cfutilities[index].append(self.Probability_Opp[index]*sign*self.infosets.Payoff_P1[index][idlist])
                        else:
                            if iteration:
                                self.cfutilities[index].append(0)
                            for idson in range(len(dslist)):
                                ds = dslist[idson]
                                payoffsums[index] += payoffsums[ds] * self.strategies[index][idlist] * self.infosets.Nature_Weight[index][idlist][idson]
                                #self.utilities[index] += self.Probability_Opp[index]*self.strategies[index][idlist]*sign*payoffsums[ds]
                                if iteration:
                                    self.cfutilities[index][idlist] += self.Probability_Opp[index]*sign*payoffsums[ds]
                    #print(self.infosets.History[index],self.utilities[index], self.strategies[index],self.cfutilities[index],"\n")
                    if iteration:
                        self.utilities[index] = payoffsums[index]*self.Probability_Opp[index]*sign
                        regrets = self.get_regrets(index)
                        self.update_strategies(index, regrets)

################################################################################
    # Infosets Opponents probabilities
    def tree_drop(self, proxy = False) :
        if proxy:
            strat = self.proxy
            self.terminals = []
        else:
            strat = self.strategies
        self.Probability_Opp = [0.0 for _ in range(len(self.infosets.index))]
        self.Probability_P1 = [0.0 for _ in range(len(self.infosets.index))]
        self.Probability_P2 = [0.0 for _ in range(len(self.infosets.index))]
        roots = self.infosets.index[self.infosets.Depth == 1]
        for startingidx in roots:
            tot_p = 0
            for im in self.infosets.Index_Members[startingidx]:
                tot_p += self.nodes.Nature_Prob[im]
            self.Probability_Opp[startingidx] = tot_p
            self.Probability_P1[startingidx] = tot_p
            self.Probability_P2[startingidx] = tot_p
        for depth in range(1,max(self.infosets['Depth']) + 1):
            icurinfosets = list(self.infosets.index[self.infosets['Depth'] == depth])
            for icurinfo in icurinfosets :
                dslists = self.infosets.Direct_Sons[icurinfo]
                for idslist in range(len(dslists)) : # select one action
                    dslist = dslists[idslist]
                    if len(dslist) > 0:
                        for idson in range(len(dslist)) : # select one son infoset
                            dson = dslist[idson]
                            if self.infosets.Player[icurinfo] == 1 :
                                self.Probability_P1[dson] += self.Probability_P1[icurinfo] * strat[icurinfo][idslist] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                                self.Probability_P2[dson] += self.Probability_P2[icurinfo] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                            else :
                                self.Probability_P2[dson] += self.Probability_P2[icurinfo] * strat[icurinfo][idslist] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                                self.Probability_P1[dson] += self.Probability_P1[icurinfo] * self.infosets.Nature_Weight[icurinfo][idslist][idson]
                            if self.infosets.Player[dson] == 1 :
                                self.Probability_Opp[dson] = self.Probability_P2[dson]
                            else :
                                self.Probability_Opp[dson] = self.Probability_P1[dson]

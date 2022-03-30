##Useless
################################################################################
    '''
    def init_sigma(self, node, output = None):
        output = dict()
        def init_sigma_recursive(node):
            if self.nodes.Dad[node] != 999999:
                #print(self.nodes.Dad[node])
                if self.nodes.Type[node]=="L" or self.nodes.Abs_Map[self.nodes.Dad[node]] in self.info_leaves:
                    return
            if self.nodes.Type[node] == 'C':
                output[self.nodes.Abs_Map[node]] = {self.nodes.Actions[node][idaction]: self.nodes.Actions_Prob[node][idaction] for idaction in range(len(self.nodes.Actions[node]))}
            else:
                output[self.nodes.Abs_Map[node]] = {action: 1. / len(self.nodes.Actions[node]) for action in self.nodes.Actions[node]}
            for ds in self.nodes.Direct_Sons[node]:
                init_sigma_recursive(ds)
        init_sigma_recursive(node)
        return output
    '''
'''
    def empty_strategies_init(self, node, output = None):
        #print(self.info_roots)
        output = dict()
        def strategies_init(node):
            #print(node, self.nodes.Abs_Map[node])
            if self.nodes.Dad[node] != 999999:
                if self.nodes.Type[node] == 'L' or self.nodes.Abs_Map[self.nodes.Dad[node]] in self.info_leaves:
            #        print(node)
                    return
            output[self.nodes.Abs_Map[node]] = {action: 0. for action in self.nodes.Actions[node]}
            for ds in self.nodes.Direct_Sons[node]:
                strategies_init(ds)
        strategies_init(node)
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
'''
'''
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
                        else:
                            self.cfutilities[icurinfo].append(0)
                            for idson in range(len(dslist)) : # select one son infoset
                                dson = dslist[idson]

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

                                dads[dson].append(icurinfo)
                                dad_probs[dson].append(self.proxy[icurinfo][idslist]*self.infosets.Nature_Weight[icurinfo][idslist][idson])
                                dad_actions[dson].append(idslist)

        for t in terminals:
            regrets = get_regrets(t, payoff)
            update_strategies(t, regrets)

def prob_check(dataframe):
    for dpt in range(0, max(dataframe['Depth'])):
        depthdf = dataframe[dataframe.Depth == dpt]
        print(depthdf.Probability)
        sum = 0
        for prob in depthdf.Probability:
            sum = sum + prob
        print("Total Probability at depth ", dpt)
        print(" is ", sum)

def payoffvectors(infosets,nodes):
    pv1 = []
    terminals = nodes[nodes.Type == 'L']
    #pv2 = [[] for _ in range(len(infosets.index))]
    for index,row in infosets.iterrows():
        for member in row.Members:
            payoff = []
            for tindex,terminal in terminals.iterrows():
                if terminal.History.find(member) != -1:
                    c1 = terminal.Payoff_P1
                    #c2 = -c1
                    payoff.append(c1)
                #
            #
        #
        pv1.append(payoff)
    #
    infosets['Payoff_Vector_P1'] = pv1

def payoffvectors(nodes):
    last = '(?<=\:)(.*)$'
    pv1 = [[[] for _ in range(0,100)] for _ in range(len(nodes.index))]
    for leaf in nodes.iloc[nodes.index[nodes.Type == 'L'].tolist()]:
        def recursivepo(dad):

            if dad.Sons == []:
                for member in dad.Index_Members:



            for idxson in dad.Sons:
                if(infosets.Depth[idxson] == dad.Depth + 1):
                    son = infosets.iloc[idxson]

                    pv1[dad.name][] = pv1[dad.name] + recursivepo(son) + [idxson]

            return pv1[dad.name]

        recursivepo(root)

    infosets['Payoff_Vector_P1'] = pv1
'''

'''
def nodedescendents(nodes) : ##outdated
    descendent = [[] for _ in range(len(nodes.index))]
    for index,row in nodes[nodes.Type == 'L'].iterrows() :
        if(row.History == '/'):
            descendent[index] = nodes.index.values
        else:
            nd = nodes.where(nodes.History.str.find(row.History + '/') != -1)
            nd = nd.dropna()
            descendent[index] = nd.index.values
    #
    nodes['Sons'] = descendent

    def ispayoffs(infosets, nodes):
        ispo1 = [[] for _ in range(len(infosets.index))]
        for index,row in infosets.iterrows():
            for i in row.Index_Members:
                ispo1[index] += nodes.Payoff_Vector_P1[i]
            #
        #
        infosets['Payoff_Vector_P1'] = ispo1
'''
'''
def histoparents(infosets):
    opparents  = [[] for _ in range(len(infosets.index))]
    oppactions = [[] for _ in range(len(infosets.index))]
    for index, row in infosets.iterrows():
        hist = row.History[4:]
        regexchance = 'C:'
        regex = '(?<=\:)(.){1,6}$'
        ix = hist.find(regexchance)
        if ix != -1:
            hist = hist[:ix] + hist[ix+4:]
        if row.Player == 1:
            opponent = 2
        else:
            opponent = 1
        for pindex, prow in infosets[infosets.Depth < row.Depth].iterrows():
            phist = prow.History[4:]
            pix = phist.find(regexchance)
            if pix != -1:
                phist = phist[:ix] + phist[ix+4:]
            if phist in hist and prow.Player == opponent and phist != "" and hist != "":
                opparents[index].append(pindex)
                match = re.search(regex, phist)
                oppactions[index].append(match[0])

    infosets['Opponent_Parents'] = opparents
    infosets['Opponent_Actions'] = oppactions

'''
'''
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

'''
'''
    def recursive_utility_call(self,startingabsidx, init = False, oppo_prob = True):

        if init:
            self.utilities = np.zeros(len(self.infoset.index))

        if oppo_prob:
            prob = self.infosets.Probability_Opp
        else:
            prob = self.infosets.Probability

        def recursive_utility(absidx, sonut = 0) :
            dslists = self.infosets.Direct_Sons[absidx]
            for idslist in range(len(dslists)) :
                dslist = dslists[idslist]
                if len(dslist) == 0: ## so the action number idslist leads to terminal nodes aka a single abstract payoff
                    self.infosets.Exp_Utility[absidx] += self.infosets.Payoff_P1[idslist]*self.infosets.Actions_Prob[idslist]
                else:
                    for idson in range(len(dslist)): #cycling on sons
                        self.infosets.Exp_Utility[absidx] += self.infosets.Exp_Utility[idson]*self.infosets.Actions_Prob[idslist]
                        recursive_utility(idson, sonut)

        recursive_utility(startingabsidx)
'''


'''
################################################################################
    def update_abstract(self, abs_index, regrets):
        self.update_strategies(abs_index, regrets)
        for i in self.infosets.Index_Members[abs_index]:
            self.nodes.Actions_Prob[i] = self.strategies[abs_index]
            self.recursive_probs(i)
            utility = 0.
            for son in self.nodes.Sons[i]:
                if self.nodes.Type[son] == 'L':
                    utility += self.nodes.Payoff_Vector_P1[son]*self.nodes.Probability[son]
            self.nodes.Exp_Utility[i] = utility
################################################################################
'''

'''
###############################################################################

    def recursive_probs_oppo_abstract_call(self, startingnodeidx, init = False) :

        if init :
            self.Probability_Opp = [0.0 for _ in range(len(self.infosets.index))]

            tot_p = 0
            for im in self.infosets.Index_Members[startingnodeidx]:
                tot_p += self.nodes.Nature_Prob[im]
            self.Probability_Opp[startingnodeidx] = tot_p

        def recursive_probs_oppo_abstract(idxcurnode, prevprob = 1) :
            dslists = self.infosets.Direct_Sons[idxcurnode]
            for idslist in range(len(dslists)) : # select one action
                if len(dslists) > 0 :
                    dslist = dslists[idslist]
                    if len(dslist) > 0 :
                        for idson in range(len(dslist)) : # select one son infoset
                            dson = dslist[idson]
                            prevprobnow = prevprob
                            if self.infosets.Player[idxcurnode] != selectplayer:
                                prevprobnow = prevprob * self.strategies[idxcurnode][idslist] * self.infosets.Nature_Weight[idxcurnode][idslist][idson]
                            if self.infosets.Player[dson] == selectplayer :
                                self.Probability_Opp[dson] += prevprobnow
                            recursive_probs_oppo_abstract(dson,prevprobnow)

        selectplayer = 1
        recursive_probs_oppo_abstract(startingnodeidx, prevprob = self.Probability_Opp[startingnodeidx])
        selectplayer = 2
        recursive_probs_oppo_abstract(startingnodeidx, prevprob = self.Probability_Opp[startingnodeidx])
'''
'''
###############################################################################
    # Infosets Opponents probabilities

    def tree_drop(self, dpt = 0, init = True) :
        first = min(self.infosets.index[self.infosets.Depth == dpt + 1])
        self.Probability_Opp[first:] = [0.0 for _ in range(len(self.infosets.index[first:]))]
        self.Probability_P1[first:] = [0.0 for _ in range(len(self.infosets.index[first:]))]
        self.Probability_P2[first:] = [0.0 for _ in range(len(self.infosets.index[first:]))]
        if init:
            roots = self.infosets.index[self.infosets.Depth == dpt + 1]
            for startingidx in roots:
                tot_p = 0
                for im in self.infosets.Index_Members[startingidx]:
                    tot_p += self.nodes.Nature_Prob[im]
                self.Probability_Opp[startingidx] = tot_p
                self.Probability_P1[startingidx] = tot_p
                self.Probability_P2[startingidx] = tot_p
        for depth in range(dpt, max(self.infosets['Depth']) + 1):
            icurinfosets = list(self.infosets.index[self.infosets['Depth'] == depth])
            for icurinfo in icurinfosets :
                dslists = self.infosets.Direct_Sons[icurinfo]
                for idslist in range(len(dslists)) : # select one action
                    dslist = dslists[idslist]
                    for idson in range(len(dslist)) : # select one son infoset
                        dson = dslist[idson]
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
'''
    def sample_actions(self, opponent):
        self.proxy = [np.zeros(len(self.strategies[_])) for _ in range(len(self.strategies))]
        depths = self.infosets.Depth[self.infosets.Player == opponent]
        #print(depths)
        for dpt in depths:
            n_samples_dpt = math.ceil(n_samples*(len(self.infosets[self.infosets.Depth == dpt])/len(self.infosets.index)))
            #print(n_samples_dpt)
            for i in range(n_samples_dpt):
                abs_index = int(np.random.choice(self.infosets.index[(self.infosets.Player == opponent) & (self.infosets.Depth == dpt)], 1))
                #print(abs_index)
                act_index = int(np.random.choice(range(len(self.strategies[abs_index])), 1))
                #print(act_index)
                self.proxy[abs_index][act_index] = self.strategies[abs_index][act_index]

            indices = self.infosets.index[self.infosets.Player != opponent]
            for i in indices:
                self.proxy[i] = self.strategies[i]
'''
'''




    def infotonodes(self):
        for rootlist in self.info_roots:
            temp = []
            for root in rootlist:
                for im in self.infosets.Index_Members[root]:
                    temp.append(im)
            self.node_roots.append(temp)

        for sonslist in self.info_sons:
            temp = []
            for son in sonslist:
                for im in self.infosets.Index_Members[son]:
                    temp.append(im)
            self.node_sons.append(temp)



    def coparents(self):
        for d in range(max(self.infosets.Depth)):
            for index, row in self.infosets.iterrows():
                if self.isroot[index] == False:
                    self.isroot[index] = True
                    coroots, sonroots = self.rooter(index)
                    self.info_roots.append(coroots)
                    #self.info_sons.append(sonroots)



    def rooter(self, froot):
        coroots = [froot]
        queueroots = [froot]
        sonroots = []
        while queueroots :
            root = queueroots.pop(0)
            for idlist in range(len(self.infosets.Direct_Sons[root])):
                dslist = self.infosets.Direct_Sons[root][idlist]
                if len(dslist) > 0:
                    for idson in range(len(dslist)):
                        dson = dslist[idson]
                        sonroots.append(dson)
                        for daddylist in self.infosets.Dads[dson]:
                            if isinstance(daddylist, int):
                                if not self.isroot[daddylist] and self.infosets.Player[daddylist] == self.infosets.Player[root]:
                                    self.isroot[daddylist] = True
                                    coroots.append(daddylist)
                            else:
                                for daddy in daddylist:
                                    if not self.isroot[daddy] and self.infosets.Player[daddy] == self.infosets.Player[root]:
                                        self.isroot[daddy] ==True
                                        coroots.append(daddy)
                                        queueroots.append(daddy)
                        #self.rooter(dson)
        #
        return coroots, sonroots
'''

    #def exp_utilities(self):

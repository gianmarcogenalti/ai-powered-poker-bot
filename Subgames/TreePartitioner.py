import Utilities as U
import pandas as pd

class TreePartitioner:

    def __init__(self,abs_infosets, depth_lim = False, max_depth = 100):
        self.infosets = abs_infosets
        self.info_roots = [[] for _ in range(len(self.infosets.index))]
        self.info_leaves = [[] for _ in range(len(self.infosets.index))]
        self.isroot = [False for _ in range(len(self.infosets.index))]
        self.info_subgames = [[] for _ in range(len(self.infosets.index))]
        self.depth_subgames = [[] for _ in range(len(self.infosets.index))]
        self.subgameid = [[] for _ in range(len(self.infosets.index))]
        self.depth_limited = depth_lim
        self.subgameplayer = [0 for _ in range(len(self.infosets.index))]
        if depth_lim:
            self.max_depth = max_depth
            self.subgamedepth = [0 for _ in range(len(self.infosets.index))]



    def subgamegenerator(self):
        counter = 0
        for index, row in self.infosets.iterrows():
            if not self.isroot[index]:
                self.subgameplayer[counter] = self.infosets.Player[index]
                if self.depth_limited:
                    self.subgamedepth[counter] = self.infosets.Depth[index]
                self.rooter(index, counter)
                counter += 1
        self.info_subgames = [x for x in self.info_subgames if x != []]
        self.info_roots = [x for x in self.info_roots if x != []]
        self.info_leaves = [x for x in self.info_leaves if x != []]


    def rooter(self,index, counter):
        if index not in self.info_subgames[counter]:
            if self.infosets.Direct_Sons[index].count([]) == len(self.infosets.Direct_Sons[index]) and index not in self.info_leaves[counter]:
                self.info_leaves[counter].append(index)
            self.subgameid[index].append(counter)
            self.info_subgames[counter].append(index)
            #self.depth_subgames[counter].append(self.infosets.Depth[index])
            for idlist in range(len(self.infosets.Direct_Sons[index])):
                dslist = self.infosets.Direct_Sons[index][idlist]
                for idson in range(len(dslist)):
                    ds = dslist[idson]
                    if self.depth_limited and (self.infosets.Depth[ds] <= self.subgamedepth[counter] + self.max_depth): #and self.infosets.Player[index] != self.infosets.Player[self.info_roots[counter][0]]):
                        if not (self.infosets.Depth[ds] == self.subgamedepth[counter] + self.max_depth and self.infosets.Player[ds] != self.subgameplayer[counter]):
                            self.rooter(ds, counter)
                    elif index not in self.info_leaves[counter]:
                        #print(counter,index)
                        self.info_leaves[counter].append(index)
                    if not self.depth_limited:
                        self.rooter(ds, counter)
                    if ds in self.info_roots[counter]:
                        self.info_roots[counter].remove(ds)
            if not bool(U.intersection(self.infosets.Dads[index],self.info_subgames[counter])):
                self.isroot[index] = True
                self.info_roots[counter].append(index)
            else:
                for dad in self.infosets.Dads[index]:
                    self.rooter(dad, counter)

    def chanceroot(self, nodes):
        #subgamesid = [[] for _ in range(len(nodes))]
        for idroots in range(len(self.info_roots)):
            roots = self.info_roots[idroots]
            noderoots = []
            for root in roots:
                noderoots = noderoots + self.infosets.Index_Members[root]
            #indices = nodes.iloc[noderoots, -1].index.values
            #for i in indices:
                #subgamesid[i].append(idroots)
            totprob = 0
            for node in noderoots:
                totprob += nodes.Probability[node]
            #print(totprob)
            chprobs = []
            if totprob > 0:
                for node in noderoots:
                    chprobs.append(nodes.Probability[node]/totprob)
            else:
                for node in noderoots:
                    chprobs.append(1/len(noderoots))
            #if not totprob:
            cdf = pd.DataFrame([[chprobs]], columns = ['Actions_Prob'])
            cdf['Actions'] = [list(map(str,noderoots))]
            cdf['Direct_Sons'] = [noderoots]
            cdf['Type'] = "C"
            cdf['Dad'] = 999999
            cdf['Player'] = 0
            cdf['Depth'] = self.infosets.Depth[roots[0]]
            #cdf['Subgames'] = idroots
            #print(cdf)
            nodes = nodes.append(cdf, ignore_index=True)
        #nodes['Subgames'] = subgamesid

        return nodes

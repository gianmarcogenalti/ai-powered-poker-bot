import Utilities as U

class TreePartitioner:

    def __init__(self,abs_infosets, depth_lim = False, max_depth = 100):
        self.infosets = abs_infosets
        self.info_roots = [[] for _ in range(len(self.infosets.index))]
        self.isroot = [False for _ in range(len(self.infosets.index))]
        self.info_subgames = [[] for _ in range(len(self.infosets.index))]
        self.depth_subgames = [[] for _ in range(len(self.infosets.index))]
        self.subgameid = [[] for _ in range(len(self.infosets.index))]
        self.depth_limited = depth_lim
        if depth_lim:
            self.max_depth = max_depth
            self.subgamedepth = [0 for _ in range(len(self.infosets.index))]
            self.subgameplayer = [0 for _ in range(len(self.infosets.index))]


    def subgamegenerator(self):
        counter = 0
        for index, row in self.infosets.iterrows():
            if not self.isroot[index]:
                if self.depth_limited:
                    self.subgamedepth[counter] = self.infosets.Depth[index]
                    self.subgameplayer[counter] = self.infosets.Player[index]
                self.rooter(index, counter)
                counter += 1
        self.info_subgames = [x for x in self.info_subgames if x != []]
        self.info_roots = [x for x in self.info_roots if x != []]


    def rooter(self,index, counter):
        if index not in self.info_subgames[counter]:
            self.subgameid[index].append(counter)
            self.info_subgames[counter].append(index)
            #self.depth_subgames[counter].append(self.infosets.Depth[index])
            for idlist in range(len(self.infosets.Direct_Sons[index])):
                dslist = self.infosets.Direct_Sons[index][idlist]
                for idson in range(len(dslist)):
                    ds = dslist[idson]
                    if self.depth_limited and (self.infosets.Depth[ds] <= self.subgamedepth[counter] + self.max_depth): #and self.infosets.Player[index] != self.infosets.Player[self.info_roots[counter][0]]):
                        if not (self.infosets.Depth[ds] == self.subgamedepth[counter] + self.max_depth and self.infosets.Player[ds] == self.subgameplayer[counter]):
                                self.rooter(ds, counter)
                    elif not self.depth_limited:
                        self.rooter(ds, counter)
                    if ds in self.info_roots[counter]:
                        self.info_roots[counter].remove(ds)
            if not bool(U.intersection(self.infosets.Dads[index],self.info_subgames[counter])):
                self.isroot[index] = True
                self.info_roots[counter].append(index)
            else:
                for dad in self.infosets.Dads[index]:
                    self.rooter(dad, counter)
'''
    def tree_pruning(self, max_depth):
        for idlist in range(len(self.depth_subgames)):
            root_depth = min(self.depth_subgames[idlist])
            print(root_depth)
            for idis in range(len(self.info_subgames[idlist])):
    '''

class TreePartitioner:

    def __init__(self,abs_infosets):
        self.infosets = abs_infosets
        self.isroot = [False for i in range(len(self.infosets.index))]
        self.info_roots = []
        self.info_sons = []
        self.info_subgames = []
        self.node_roots = []
        self.node_sons = []

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
                    self.info_sons.append(sonroots)



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

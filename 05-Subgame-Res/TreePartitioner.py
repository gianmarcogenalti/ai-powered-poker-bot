class TreePartitioner:

    def __init__(self,abs_infosets):
        self.infosets = abs_infosets
        self.isroot = [False for i in range(len(self.infosets.index))]
        self.coroots = []

    def coparents(self):
        for d in range(max(self.infosets.Depth)):
            for index, row in self.infosets.iterrows():
                if self.isroot[index] == False:
                    self.isroot[index] = True
                    self.coroots.append(self.rooter(index))



    def rooter(self, root):
        coroots = [root]
        for idlist in range(len(self.infosets.Direct_Sons[root])):
            dslist = self.infosets.Direct_Sons[root][idlist]
            if len(dslist) > 0:
                for idson in range(len(dslist)):
                    dson = dslist[idson]
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
        #
        return coroots

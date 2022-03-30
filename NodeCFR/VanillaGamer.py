from NodeCFR.Gamer import *
import time

class VanillaGamer(Gamer):
    def __init__(self, nodes):
        super().__init__(nodes, chance_sampling = False)



    def run(self, iterations = 1):
        t0 = time.time()
        for _ in range(0, iterations):
            print("Iteration %d" % _)
            self._cfr_utility_recursive(self.root, 1, 1)
            # since we do not update sigmas in each information set while traversing, we need to
            # traverse the tree to perform to update it now
            self.__update_sigma_recursively(self.root)
        print("Execution time: %d" % (time.time() - t0))




    def __update_sigma_recursively(self, node):
        # stop traversal at terminal node
        if self.nodes.Type[node] == 'L':
            return
        # omit chance
        if not self.nodes.Type[node] == 'C':
            self._update_sigma(self.nodes.Abs_Map[node])
        # go to subtrees
        for ds in self.nodes.Direct_Sons[node]:
            self.__update_sigma_recursively(ds)

import time
from NodeCFR.CounterfactualRegretMinimizationBase import *

class ChanceSamplingCFR(CounterfactualRegretMinimizationBase):
    def __init__(self, nodes,abs_infosets, roots, leaves, players, it):
        super().__init__(nodes, abs_infosets,roots, leaves,players, it, chance_sampling = True)


    def run(self, iterations = 1):
        t0 = time.time()
        for _ in range(0, iterations):
            if not _ % 200:
                print("Iteration %d.%d" % (self.it, _))
            self._cfr_utility_recursive(self.root, 1, 1)

        print("Execution time: %d" % (time.time() - t0))

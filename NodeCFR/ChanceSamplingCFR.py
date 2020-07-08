import time
from NodeCFR.CounterfactualRegretMinimizationBase import *

class ChanceSamplingCFR(CounterfactualRegretMinimizationBase):
    def __init__(self, nodes):
        super().__init__(nodes, chance_sampling = True)


    def run(self, iterations = 1):
        t0 = time.time()
        for _ in range(0, iterations):
            if _%500 == 0:
                print("Iteration %d" % _)
            self._cfr_utility_recursive(self.root, 1, 1)

        print("Execution time: %d" % (time.time() - t0))

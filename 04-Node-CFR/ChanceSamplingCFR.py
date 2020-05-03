class ChanceSamplingCFR(CounterfactualRegretMinimizationBase):
    def __init__(self, root):
        super().__init__(root = root, chance_sampling = True)


    def run(self, iterations = 1):
        for _ in range(0, iterations):
            self._cfr_utility_recursive(self.root, 1, 1)

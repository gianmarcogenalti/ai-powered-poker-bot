import time
from NodeCFR.Gamer import *

class CSGamer(Gamer):
    def __init__(self, nodes):
        super().__init__(nodes, chance_sampling = True)

    def run(self, iterations = 1):
        conv = False
        t0 = time.time()
        count = 0
        while not conv:
            for _ in range(count*iterations, (count+1)*iterations):
                if _%500 == 0:
                    print("Iteration %d" % _)
                self._cfr_utility_recursive(self.root, 1, 1,_)
                #(E.exploiter(self.nodes,self.sigma, self.root, 1)+ E.exploiter(self.nodes,self.sigma, self.root, 2)-2*self.exp_ut())/2
            #print(self.cumulative_regrets, self.cumulative_sigma)
            try:
                self.compute_nash_equilibrium()
                conv = True
            except:
                print('Convergence not reached in %d iterations, continue training' % ((count+1)*iterations))
                count +=1
                pass

        print("Execution time: %d" % (time.time() - t0))

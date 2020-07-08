from Clustering.clusterinfosets import *
import Utilities as U
import time

def abstractgeneration(infosets, verbose = False, sizeofabstraction = 0.5):

    t0 = time.time()
    # We initialize the abstract structure
    abs_infosets = pd.DataFrame()
    abs_infosets['History_Structure'] = U.createstringflag(infosets['History'])
    abs_infosets['Depth'] = infosets['Depth']
    abs_infosets['Payoff'] = infosets['Payoff_Vector_P1']
    abs_infosets['Player'] = infosets['Player']
    abs_infosets['Real_Parents'] = infosets['Direct_Parents']
    abs_infosets['Actions'] = infosets['Actions']
    abs_infosets['Probability'] = infosets['Probability']
    abs_infosets['MapPh1'] = [[] for i in range(len(abs_infosets['History_Structure']))]
    abs_infosets['Map'] = [[] for i in range(len(abs_infosets['History_Structure']))]

    #print(abs_infosets.shape)
    # Merges infosets without loss of information
    abs_infosets = cluster(abs_infosets, infoloss = False)
    #print(abs_infosets.shape)
    # Properly clusters infosets
    abs_infosets = cluster(abs_infosets, infoloss = True, sizeofabstraction = sizeofabstraction)
    #print(abs_infosets.shape)
    # Collects the initial data left behind
    abs_infosets = infosetstoprint(abs_infosets, infosets)

    # Saves it
    #infosets.to_csv("..\\Import-files\\clust_"+game+".csv", index = False, header = True)
    if verbose:
        print(abs_infosets)
        dt = time.time() - t0
        print("Execution time: %f" % dt)
    return abs_infosets

from Clustering.clusterinfosets import *
import time

def abstractgeneration(infosets, verbose = False):
    t0 = time.time()
    abs_infosets = pd.DataFrame()
    abs_infosets['History_Structure'] = infosets['History']
    abs_infosets['Depth'] = infosets['Depth']
    abs_infosets['Payoff'] = infosets['Payoff_Vector_P1']
    abs_infosets['Player'] = infosets['Player']
    abs_infosets['Real_Parents'] = infosets['Direct_Parents']
    abs_infosets['Actions'] = infosets['Actions']
    abs_infosets['Probability'] = infosets['Probability']
    abs_infosets['MapPh1'] = [[] for i in range(len(abs_infosets['History_Structure']))]
    abs_infosets['Map'] = [[] for i in range(len(abs_infosets['History_Structure']))]

    # Merges infosets without loss of information
    abs_infosets = cluster(abs_infosets, infoloss = False)

    # Properly clusters infosets
    abs_infosets = cluster(abs_infosets, infoloss = True)

    # Collects the initial data left behind
    abs_infosets = infosetstoprint(abs_infosets,infosets)

    # Saves it
    #infosets.to_csv("..\\Import-files\\clust_"+game+".csv", index = False, header = True)
    if verbose:
        print(abs_infosets)
        print("Execution time: %d" %  time.time()-t0)
    return abs_infosets

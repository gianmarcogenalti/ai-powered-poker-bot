## Utilities that provide parents, sons of an infoset or a node

def sons(infosets, index) :
    descendents = []
    for member in infosets['Members'][index] :
        counter = 0
        for candidates in infosets['Members'] :
            if(counter != index) :
                for membcandidate in candidates :
                    if(membcandidate.find(member) != -1 and counter not in descendents and infosets['Player'][counter] == infosets['Player'][index]) :
                        descendents.append(counter)
                    #
                #
            #
            counter =  counter + 1
        #
    #
    return descendents

def parents(infosets, index) :
    antenates = []
    for member in infosets['Members'][index] :
        counter = 0
        for candidates in infosets['Sons'] :
            if(index in candidates and counter not in antenates) :
                antenates.append(counter)
            #
            counter = counter + 1
        #
    #
    return antenates

###### IMPORTANT: infosets' parents and sons only include SAME PLAYER infosets,
###### while in nodes also nodes of the other player.

def nodesons(nodes, index) :
    src = nodes['History'][index]
    dpt = nodes['Depth'][index]
    descendents = []
    for nindex, row in nodes[nodes['Depth'] > dpt].iterrows():
        line = row['History']
        if(line.find(src) != -1 and index != nindex):
            descendents.append(nindex)
        #
    #
    return descendents

def nodeparents(nodes, index) :
    antenates = []
    dpt = nodes['Depth'][index]
    for nindex, row in nodes[nodes['Depth'] < dpt].iterrows():
        if(index in row['Sons'] and nindex not in antenates):
            antenates.append(nindex)
        #
    #
    return antenates

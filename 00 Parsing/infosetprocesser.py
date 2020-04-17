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

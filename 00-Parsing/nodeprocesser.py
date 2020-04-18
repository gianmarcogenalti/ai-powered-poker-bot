
def sons(nodes, index) :
    descendents = []
    counter = 0;
    for candidate in nodes['History'] :
        if(counter != index) :
            if(candidate.find(member) != -1 and counter not in descendents and infosets['Player'][counter] == infosets['Player'][index]) :
                    descendents.append(counter)
            #
        #
        counter =  counter + 1
    #
    return descendents

def print_output(game, true_infosets):
    filename = "output - " + game + ".txt"
    file1 = open(filename,"a")
    file1.truncate(0)
    for index, row in true_infosets.iterrows():
        line = "infoset " + row.History + " strategies"
        #clust = row.Map_Clust
        #print(abs_infosets.Actions[clust])
        #print(output[clust])
        na = len(row.Actions)
        counter = 1
        sm = 0
        for idaction,action in enumerate(row.Actions):
            if counter != na:
                val = round(row.Actions_Prob[action],4)
                line += " " + action + "=" + str(val)
                sm += val
            else:
                line += " " + action + "=" + str(round(1 - sm,4))
            counter+=1
        file1.write(line + "\n")

    file1.close()

def print_output_bp(game, true_infosets, abs_infosets):
    filename = "output - " + game + ".txt"
    file1 = open(filename,"a")
    file1.truncate(0)
    strats = []
    for index, row in true_infosets.iterrows():
        line = "infoset " + row.History + " strategies"
        clust = row.Map_Clust
        #print(abs_infosets.Actions[clust])
        #print(output[clust])
        na = len(row.Actions)
        counter = 1
        sm = 0
        strats.append(abs_infosets.Actions_Prob[row.Map_Clust])
        for idaction,action in enumerate(row.Actions):
            if counter != na:
                val = round(abs_infosets.Actions_Prob[row.Map_Clust][action],4)
                line += " " + action + "=" + str(val)
                sm += val
            else:
                line += " " + action + "=" + str(round(1 - sm,4))
            counter +=1
        file1.write(line + "\n")

    file1.close()
    true_infosets['Actions_Prob'] = strats

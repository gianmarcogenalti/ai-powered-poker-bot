def print_output(game, output, true_infosets, abs_infosets):
    filename = "output - " + game + ".txt"
    file1 = open(filename,"a")
    file1.truncate(0)
    for index, row in true_infosets.iterrows():
        line = "infoset " + row.History + " strategies"
        clust = row.Map_Clust
        #print(abs_infosets.Actions[clust])
        #print(output[clust])
        for idaction in range(len(row.Actions)):
            action = row.Actions[idaction]
            line += " " + action + "=" + str(output[str(clust)][action])
        file1.write(line + "\n")

    file1.close()

def print_output_bp(game, true_infosets, abs_infosets):
    filename = "output - " + game + ".txt"
    file1 = open(filename,"a")
    file1.truncate(0)
    for index, row in true_infosets.iterrows():
        line = "infoset " + row.History + " strategies"
        clust = row.Map_Clust
        #print(abs_infosets.Actions[clust])
        #print(output[clust])
        na = len(row.Actions)
        counter = 1
        sm = 0
        for idaction in range(na):
            action = row.Actions[idaction]
            if counter != na:
                val = round(abs_infosets.Actions_Prob[row.Map_Clust][idaction],4)
                line += " " + action + "=" + str(val)
                sm += val
            else:
                line += " " + action + "=" + str(round(1 - sm,4))
            counter +=1
        file1.write(line + "\n")

    file1.close()

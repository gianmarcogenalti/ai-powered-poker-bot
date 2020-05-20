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

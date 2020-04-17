from infosetprocesser import sons, parents

def payoffvectors(infosets, terminals) :
    finalpv1 = []
    finalpv2 = []
    ##modpv1 = []
    #modpv2 = []
    for info in infosets['Members']:
        pv1 = []
        pv2 = []
        #mod1 = 0
        #mod2 = 0
        for member in info :
            counter = 0
            for terminal in terminals['History'] :
                if(terminal.find(member) != -1) :
                    c1 = terminals['Payoff'][counter][0]
                    c2 = terminals['Payoff'][counter][1]
                    pv1.append(c1)
                    ###mod1 = mod1 + c1*c1
                    pv2.append(c2)
                    ##mod2 = mod2 + c2*c2
                counter = counter + 1
            #end for terminals
        #end for member
        finalpv1.append(pv1)
        #modpv1.append(mod1)
        finalpv2.append(pv2)
        #modpv2.append(mod2)
        #print(finalpv1)
        #print(len(finalpv1))
    #end for info
    infosets['Payoff Vector P1'] = finalpv1
    #infosets['Payoff Modulus P1'] = modpv1
    infosets['Payoff Vector P2'] = finalpv2
    #infosets['Payoff Modulus P2'] = modpv2

def isplayers(infosets, nonterminals) :
    finalp = []
    for member in infosets['Members'] :
        counter = 0
        for nonterminal in nonterminals['History'] :
            if(nonterminal == member[0]):
                finalp.append(nonterminals['Player'][counter])
            counter = counter + 1
    infosets['Player'] = finalp

def descendents(infosets) :
    descendent = []
    for i in range(len(infosets)) :
        descendent.append(sons(infosets, i))
    #
    infosets['Sons'] = descendent

def antenates(infosets) :
    antenate = []
    for i in range(len(infosets)) :
        antenate.append(parents(infosets, i))
    #
    infosets['Parents'] = antenate
    

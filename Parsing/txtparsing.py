import re

## Utilities to read the .txt input files and provide datas to the dataframeparsing.py

def getisdepth(infosets) :
    v = []
    for line in infosets:
        if(~line.find("infoset")):
            occ = line.find("nodes")
            v.append(line.count("/", 0, occ))
    return v

def getnodedepth(history) :
    if(history == '/'):
        return 0
    else:
        depth = history.count("/")
        return depth

def getinfosets(textfile) :
    file = open(textfile)
    lines = file.readlines()
    file.close()
    t = []
    for line in lines:
        if(line.find("infoset")==0):
            t.append(line)
    return t

def getishist(infosets) :
    hist = []
    regex = "(?<=infoset\s)(.*?)(?=\snodes)"
    for it in infosets :
        match = re.search(regex, it)
        hist.append(match.group(1))
    return hist

def getismembers(infosets) :
    members = []
    regex = "(?<=nodes\s)(.*)"
    for line in infosets :
        member = []
        match = re.search(regex, line)
        node = match.group(1).split(' ')

        for c in range(0,len(node)) :
            member.append(node[c])

        members.append(member)
    return members

def getnodes(textfile) :
    file = open(textfile)
    lines = file.readlines()
    file.close()
    t = []
    for line in lines:
        if(line.find("node")==0):
            t.append(line)
    return t

def getterminals(nodes) :
    t = []
    for line in nodes:
        if(line.find("leaf")!= -1):
            t.append(line)

    return t

def getnonterminals(nodes) :
    nt = []
    for line in nodes:
        if(line.find("player")!=-1):
            nt.append(line)

    return nt

def getplayers(nodes) :
    p = []
    regex = "(?<=player\s)[1-2]{1}"
    for line in nodes:
        if(line.find("leaf")!= -1):
            p.append(-1)
        if(line.find("chance actions")!=-1):
            p.append(0)
        if(line.find("player")!=-1):
            match = re.findall(regex, line)
            p.append(int(match[0]))

    return p

def getnodeshist(nodes) :
    hist = []
    regex = "(?<=node\s)(.*?)(?=\s)"
    for it in nodes :
        match = re.search(regex, it)
        hist.append(match.group(0))
    return hist

def getoddactions(nodes) :
    a = []
    o = []
    regex = "(?<=actions\s)(.*)"
    for line in nodes :
        action = []
        odd = []
        match = re.search(regex, line)
        node = match.group(1).split(' ')

        for c in range(0,len(node)) :
            act = re.split('=', node[c])
            action.append(act[0])
            odd.append(float(act[1]))

        a.append(action)
        o.append(odd)

    return a,o

def getactions(nodes) :
    a = []
    regex = "(?<=actions\s)(.*)"
    for line in nodes :
            action = []
            match = re.search(regex, line)
            node = match.group(1).split(' ')

            for c in range(0,len(node)) :
                action.append(node[c])

            a.append(action)
    return a

def getnodesactions(nodes) :
    a = []
    o = []
    regex = "(?<=actions\s)(.*)"
    for line in nodes :
        if(line.find("leaf")!= -1):
            a.append('Leaf')
            o.append('Leaf')
        else:
            action = []
            odd = []
            match = re.search(regex, line)
            node = match.group(1).split(' ')

            for c in range(0,len(node)) :
                act = re.split('=', node[c])
                action.append(act[0])
                if(line.find("chance actions")!= -1):
                    odd.append(float(act[1]))
                else:
                    odd.append(1.00)

            o.append(odd)
            a.append(action)
    return a,o

def oddtoprob(odds):
    prob = []
    for odd in odds:
        if(odd == 'Leaf'):
            prob.append('END')
        else:
            p = []
            tot = sum(odd)
            for o in odd:
                p.append(o/tot)
            #
            prob.append(p)
    #
    return prob

def getpayoff(nodes) :
    po = []
    regex1 = "(?<=1=)(.*)(?=\s2)"
    regex2 = "(?<=2=)(.*)$"
    for line in nodes :
        if(line.find("leaf")!= -1):
            match1 = re.findall(regex1,line)
            match2 = re.findall(regex2,line)
            #print(len(match1), len(match2))
            #payoff = [float(match1[0]), float(match2[0])]
            payoff = float(match1[0])
            po.append(payoff)
        else:
            po.append('NONTERMINAL')

    return po

def getchance(nodes) :
    c = []
    for line in nodes:
        if(line.find("chance actions")!=-1):
            c.append(line)

    return c

def nodeiscomp(node, infoset, player) : #node = nonterminals df row; infoset = History of the infoset; player
    ## Example with Player 1
    #/C:QK/P1:c/P2:c/C:K/P1:c/P2:raise4 <- node
    #/Q?/P1:c/P2:c/C:K/P1:c/P2:raise4  <- infoset
    line = '/' + node[3:]
    if(player == 1):
        line = line[:2] + '?' + line[3:]
    else:
        line = line[:1] + '?' +  line[2:]
    return line == infoset

def types(nodes) :
    t = []
    for line in nodes:
        if(line.find("chance actions")!=-1):
            t.append('C')
        if(line.find("leaf")!= -1):
            t.append('L')
        if(line.find("player")!=-1):
            t.append('N')
    return t

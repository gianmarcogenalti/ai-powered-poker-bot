import re
'''
def printinfosets(textfile) :
    file = open(textfile);
    lines = file.readlines();
    file.close();

    for line in lines:
        if(line.find("node")):
            line = line.strip();
            print(line);
'''
def getisdepth(infosets) :
    v = []
    for line in infosets:
        if(~line.find("infoset")):
            occ = line.find("nodes")
            v.append(line.count("/", 0, occ))
    return v

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

def getpayoff(nodes) :
    po = []
    regex1 = "(?<=1=)(.*)(?=\s2)"
    regex2 = "(?<=2=)(.*)$"
    for line in nodes :
        match1 = re.findall(regex1,line)
        match2 = re.findall(regex2,line)
        #print(len(match1), len(match2))
        payoff = [float(match1[0]), float(match2[0])]
        po.append(payoff)

    return po

def getchance(nodes) :
    c = []
    for line in nodes:
        if(line.find("chance actions")!=-1):
            c.append(line)

    return c

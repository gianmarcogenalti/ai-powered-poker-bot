import pandas as pd
from txtparsing import getinfosets, getishist, getismembers, getisdepth, getnonterminals, getnodeshist, getplayers, getactions, getnodes, getterminals, getpayoff, getchance

## Creating the four dataframes required 

def infosetdf(textfile) :

    t = getinfosets(textfile)

    data = {'History' : getishist(t),
    'Members' : getismembers(t),
    'Depth' : getisdepth(t)
    }

    df = pd.DataFrame(data,columns = ['History', 'Members', 'Depth'])

    return df

def nonterminaldf(textfile) :

    n = getnodes(textfile)
    t = getnonterminals(n)

    data = {'History' : getnodeshist(t),
    'Player' : getplayers(t),
    'Actions' : getactions(t)
    }

    df = pd.DataFrame(data, columns = ['History', 'Player', 'Actions'])

    return df

def terminaldf(textfile) :

    n = getnodes(textfile)
    t = getterminals(n)

    data = {'History' : getnodeshist(t),
    'Payoff' : getpayoff(t)
    }

    df = pd.DataFrame(data, columns = ['History', 'Payoff'])

    return df

def chancedf(textfile) :

    n = getnodes(textfile)
    t = getchance(n)

    data = {'History' : getnodeshist(t),
    'Actions' : getactions(t)
    }

    df = pd.DataFrame(data, columns = ['History', 'Actions'])

    return df

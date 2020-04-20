import pandas as pd
from txtparsing import *

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
    a,o = getoddactions(t)

    data = {'History' : getnodeshist(t),
    'Actions' : a,
    'Odds' : o
    }

    df = pd.DataFrame(data, columns = ['History', 'Actions', 'Odds'])

    return df

def nodesdf(textfile) :

    n = getnodes(textfile)
    c = getchance(n)
    a,o = getnodesactions(n)
    p = oddtoprob(o)
    po = getpayoff(n)
    player = getplayers(n)

    data = {'History' : getnodeshist(n),
            'Type' : types(n),
            'Actions' : a,
            'Actions_Prob' : p,
            'Payoff_P1' : po,
            'Player' : player}

    df = pd.DataFrame(data, columns = ['History', 'Type', 'Actions', 'Actions_Prob', 'Payoff_P1', 'Player'])

    return df

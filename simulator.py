import argparse
import re
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-p1", "--player1", default = 'output - leduc3.txt')
ap.add_argument("-p2", "--player2", default = 'output - leduc3.txt')
ap.add_argument("-i", "--game", default = 'input - leduc3.txt')
ap.add_argument("-n", "--number", default = 100)

args = vars(ap.parse_args())
print(args)

gamestatus = dict()

restrat = "(?<=strategies\s)(.*)$"
remove = "(?<=\=)(.*)"
rehist = "(?<=infoset\s)(.*?)(?=\\sstrategies)"
renode = "(?<=node\s)(.*?)(?=\s)"
reactions = "(?<=actions\s)(.*)"
repayoff = "(?<=payoffs\s)(.*)"
replayer = "(?<=player\s)[1-2]{1}"

with open(args['player1']) as p1:
    line = p1.readline()
    while line:
        matchist = re.search(rehist, line)
        match = re.search(restrat, line)
        strats = match.group(1)
        moves = strats.split(' ')
        gamestatus.update({matchist.group(1) : {p:{'actions': [move.split('=')[0] for move in moves], 'odds': [float(move.split('=')[1]) for move in moves]} for p in ['P1','P2']}})
        line = p1.readline()
    p1.close()

with open(args['player2']) as p2:
    line = p2.readline()
    while line:
        matchist = re.search(rehist, line)
        match = re.search(restrat, line)
        strats = match.group(1)
        moves = strats.split(' ')
        for move in moves:
            gamestatus[matchist.group(1)]['P2'][move.split('=')[0]] = float(move.split('=')[1])
        line = p2.readline()
    p2.close()

gamenodes = dict()

with open(args['game']) as game:
    line = game.readline()
    while line != '\n':
        match = re.search(renode, line)
        reaction = re.search(reactions, line)
        if reaction:
            actions = re.search(reactions, line).group(1).split(' ')
            if line.find('chance') != -1:
                gamenodes.update({match.group(0): {'type': 'C', 'actions':[act.split('=')[0] for act in actions], 'odds' : [float(act.split('=')[1]) for act in actions]}})
            else:
                plmatch = re.search(replayer, line)
                gamenodes.update({match.group(0): {'type': 'N', 'actions':[act for act in actions], 'player' : int(plmatch.group(0))}})
        else:
            if line:
                payoff = re.search(repayoff, line).group(0).split(' ')[0]
                gamenodes.update({match.group(0): {'type': 'L', 'payoff': float(payoff.split('=')[1])}})

        line = game.readline()

    game.close()

collected_payoffs = []

for i in range(args['number']):
    type = 'C'
    move = np.random.choice(gamenodes['/']['actions'],p = [prob/sum(gamenodes['/']['odds']) for prob in gamenodes['/']['odds']])
    state = '/C:' + move
    pl1 = '/' + move[0] + '?'
    pl2 = '/?' + move[1]
    while type != 'L':
        if gamenodes[state]['type'] == 'C':
            move = np.random.choice(gamenodes[state]['actions'],p = [prob/sum(gamenodes[state]['odds']) for prob in gamenodes[state]['odds']])
            state = state + '/C:' + move
            pl1 = pl1 + '/C:' + move
            pl2 = pl2 + '/C:' + move
            type = gamenodes[state]['type']
        if gamenodes[state]['type'] == 'N':
            if gamenodes[state]['player'] == 1:
                move = np.random.choice(gamestatus[pl1]['P1']['actions'],p = [prob/sum(gamestatus[pl1]['P1']['odds']) for prob in gamestatus[pl1]['P1']['odds']])
                state = state + '/P1:' + move
                pl1 = pl1 + '/P1:' + move
                pl2 = pl2 + '/P1:' + move
                type = gamenodes[state]['type']
            else:
                move = np.random.choice(gamestatus[pl2]['P2']['actions'],p = [prob/sum(gamestatus[pl2]['P2']['odds']) for prob in gamestatus[pl2]['P2']['odds']])
                state = state + '/P2:' + move
                pl1 = pl1 + '/P2:' + move
                pl2 = pl2 + '/P2:' + move
                type = gamenodes[state]['type']
        if gamenodes[state]['type'] == 'L':
            type = 'L'
            collected_payoffs.append(gamenodes[state]['payoff'])

print(sum(collected_payoffs))

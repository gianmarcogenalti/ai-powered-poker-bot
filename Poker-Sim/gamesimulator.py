import glob
from loaddata3 import *
import random
import numpy as np
from datetime import datetime

def initialization():
    print("Welcome to the Pokerbot!\n")
    print("Wanna play or watch some matches?\n")
    for i in [0,1]:
        mat = "play" if i == 0 else "watch"
        print("%d) %s \n" % (i,mat))
    play = input('')
    if play == "0":
        print("What's your name?\n")
        name = input('\n')
        return True,name
    else:
        print("Ok, you'll watch some games!\n")
        return False, "noname"


def game_choice(play = True):
    avgames = glob.glob("**/*_infosets.csv")
    print("Available games are: \n")
    for i in range(len(avgames)):
        print("%d) %s \n" % (i, avgames[i][6:-13]))
    print("Digit the number correspondent of the game you'd like to play!\n")
    j = True
    while j:
        try:
            id = int(input(''))
        except:
            id = 'alo'
        try:
            infosets = loadinfosets(avgames[id][:-13])
            nodes = loadnodes(avgames[id][:-13])
            #print(nodes.Actions_Prob[45][0])
            j = False
        except:
            print("Choice not valid! Try again.\n")
    if play:
        print("Perfect, we will play %s! \n" % avgames[id][6:-13])
        rules(id)
    return nodes,infosets,avgames[id][6:-13]

def play_again():
    print("Wanna play another game with me? y/n \n")
    play = input('')
    if play == "y":
        return True
    else:
        print("Maybe another time!\n")
        return False

def rules(game):
    print("Do you know the rules? y/n\n")
    rules = input('')
    if rules == "n":
        print_rules(game)
        print("Press any key to continue.\n")
        anykey = input('')

def print_rules(game):
    if game == 1:
        print("In a leduc5 game there will be in play two copies of each card, with 5 different cards,the hierarchy is, worst to best:\n 9,T,J,Q,K.\nAt first each player will receive a single card and there will be the bets (checks, raises, folds), \nafter that Nature reveals another card and another phase of bets follows, clearly a couple with the table card is winning. Otherwise higher card wins.\n")
    else:
        print("In a leduc3 game there will be in play two copies of each card, with 3 different cards,the hierarchy is, worst to best:\n J,Q,K.\nAt first each player will receive a single card and there will be the bets (checks, raises, folds), \nafter that Nature reveals another card and another phase of bets follows, clearly a couple with the table card is winning. Otherwise higher card wins.\n")


def lets_play(name):
    print("Ok %s, choose a game!\n" % name)
    nodes,infosets,game = game_choice()
    #print(nodes,infosets)
    player = random.choice([1,2])
    print("You will be Player %d" % player)

    gamehist, infohist, esit = match(player, nodes, infosets, id)
    save_log(gamehist, infohist, esit, name, game)

    again = play_again()
    return again

def draw_cards(cards):
    player_card = random.choice(cards)
    cards.remove(player_card)
    print("You draw %s!\n" % player_card)
    cpu_card = random.choice(cards)
    cards.remove(cpu_card)
    return cards, player_card, cpu_card

def explore_tree(nodes,infosets,gamehist,infohist, player, cpu_player, cpu_card):
    for index,row in nodes[nodes.History == gamehist].iterrows():
        type = row['Type']
        pl = int(row.Player)
        actions = row.Actions
        probs = row.Actions_Prob
        maps = row.Map
    while type != 'L':
        #print(pl, type, player)
        if pl == player:
            print("Choose your move!\n")
            for i in range(len(actions)):
                print("%d) %s\n" % (i, actions[i]))
            isok = True
            while isok:
                try:
                    move = int(input(''))
                except:
                    move = 'not'
                try:
                    print("You have chosen %s!\n" % actions[move])
                    isok = False
                except:
                    print("Cannot choose that move. Try again\n")
            gamehist = gamehist + "/P{}:{}".format(player, actions[move])
            infohist = infohist + "/P{}:{}".format(player, actions[move])

        if pl == cpu_player:
            infos = maps
            move = np.random.choice(infosets.Actions[infos], p = infosets.Actions_Prob[infos])
            print("CPU plays %s!\n" % move)
            gamehist = gamehist + "/P{}:{}".format(cpu_player, move)
            infohist = infohist + "/P{}:{}".format(cpu_player, move)

        if type == 'C':
            move = np.random.choice(actions, p = probs)
            print("The card on the table is now %s! \n" % move)
            gamehist = gamehist + "/C:" + move
            infohist = infohist + "/C:" + move

        for index,row in nodes[nodes.History == gamehist].iterrows():
            type = row['Type']
            pl = int(row.Player)
            actions = row.Actions
            probs = row.Actions_Prob
            maps = row.Map
            po1 = row.Payoff_Vector_P1[0]


    print("CPU got in its hand %s!\n" % cpu_card)
    print(gamehist)

    sign = 1 if cpu_player == 1 else -1
    esit = sign*po1
    if po1 != 0:
        message = "You" if (po1 > 0 and player == 1) or (po1 < 0 and player == 2) else "CPU"
        print("The game has finished! %s have won with a payoff of %d\n" % (message, abs(po1)))
    else:
        print("The game ended with a Draw!\n")

    return gamehist,infohist,esit



def match(player, nodes, infosets, game):
    if game == 1:
        cards = ['9', 'T', 'J', 'Q', 'K', 'T','9', 'T', 'J', 'Q', 'K', 'T']
    else:
        cards = ['J','Q','K','J','Q','K']
    cpu_player = 2 if player==1 else 1
    cards, player_card, cpu_card = draw_cards(cards)
    if cpu_player == 1:
        gamehist = "/C:"+cpu_card+player_card
        infohist = "/"+cpu_card+"?"
    else:
        gamehist = "/C:"+player_card+cpu_card
        infohist = "/?"+cpu_card

    return explore_tree(nodes,infosets,gamehist,infohist, player, cpu_player, cpu_card)

def save_log(gamehist, infohist, esit, name, game):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    line = dt_string + ", player = " +  name + ", game = " + game + ", cpu_infoset = " + infohist + ", actual game = " + gamehist + ", cpu_esit = " + str(esit)
    logs = open("logs.txt","a")
    logs.write(line + "\n")
    logs.close()

def simulate_matches():
    nodes, info1, info2, n, cards = oppo_choose()
    cum_P1 = 0.
    #now = datetime.now()
    #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    #logs = open("head2head.txt","a")
    for i in range(2*n):
        esitP1, gamehist1, gamehist2 = play_against(nodes, info1, info2, cards)
        #line = dt_string + ", player = " +  name + ", game = " + game + ", cpu_infoset = " + infohist + ", actual game = " + gamehist + ", cpu_esit = " + str(esit)
        cum_P1 += esitP1
    #logs.write(line + "\n")
    #logs.close()
    return cum_P1




def oppo_choose():
    print("Choose two opponent which play the same game!\n")
    nodes1, infosets1, name1 = game_choice(play = False)
    nodes2, infosets2, name2 = game_choice(play = False)
    while len(nodes1.index)!= len(nodes2.index):
        print("They play different games!\n")
        nodes2, infosets2, name2 = game_choice(play = False)
    print("How many matches should they play? (they will play 2*n singles)\n")
    n = int(input(''))
    last = len(nodes1.index) - 1
    cards = ['9', 'T', 'J', 'Q', 'K', '9', 'T', 'J', 'Q', 'K']
    m = 2*n
    print("Ok, they will play against %d times!\n" % m)
    return nodes1, infosets1, infosets2, n, cards

def play_against(nodes, info1, info2, cards):
    gamehist = give_cards(cards)
    esit1, gamehist1 = machine_plays(nodes, info1, info2, gamehist)
    esit2, gamehist2 = machine_plays(nodes, info2, info1, gamehist)
    esitP1 = esit1 - esit2
    return esitP1, gamehist1, gamehist2

def give_cards(cards):
    card1 = random.choice(cards)
    card2 = random.choice(cards)
    gamehist = "/C:"+ card1 + card2
    #infohist1 = "/"+ card1 +"?"
    #infohist2 = "/?"+ card2
    return gamehist #infohist1, infohist2

def machine_plays(nodes, infosets1, infosets2, gamehist):
    for index,row in nodes[nodes.History == gamehist].iterrows():
        type = row['Type']
        pl = int(row.Player)
        actions = row.Actions
        probs = row.Actions_Prob
        infos = row.Map
    while type != 'L':
        if pl == 1:
            #print(infosets2.Actions[infos])
            move1 = np.random.choice(infosets1.Actions[infos], p = infosets1.Actions_Prob[infos])
            #print(move)
            gamehist = gamehist + "/P{}:{}".format(pl, move1)
            #infohist = infohist + "/P{}:{}".format(pl, move)
        if pl == 2:
            #print(infosets2.Actions[infos])
            move2 = np.random.choice(infosets2.Actions[infos], p = infosets2.Actions_Prob[infos])
            #print(move)
            gamehist = gamehist + "/P{}:{}".format(pl, move2)

            #infohist = infohist + "/P{}:{}".format(pl, move)
        if type == 'C':
            movec = np.random.choice(actions, p = probs)
            gamehist = gamehist + "/C:" + movec
            #infohist = infohist + "/C:" + move

        for index,row in nodes[nodes.History == gamehist].iterrows():
            type = row['Type']
            pl = int(row.Player)
            actions = row.Actions
            probs = row.Actions_Prob
            infos = row.Map
            po1 = row.Payoff_Vector_P1[0]
        #
        #print(type)
    return po1, gamehist

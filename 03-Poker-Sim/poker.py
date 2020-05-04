from gamesimulator import *

play,name = initialization()
while play:
    play = lets_play(name)
if not play and name == "noname":
    simulate_matches()

print("\n\n\n\n\n\n\nThank You!")

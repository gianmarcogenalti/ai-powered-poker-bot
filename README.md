# AI Powered 2-Players Poker Bot
## Simplified Replica of the Implementation of the well-known AI for 2-players Poker "Libratus" (https://en.wikipedia.org/wiki/Libratus).
### This AI powered bot has been developed to partecipate to the AI Poker Tournament of Politecnico di Milano in 2020, held by Prof. Nicola Gatti. This implementation resulted as the winner of that edition.
### The procedure is summarized as follows:
### 00-Parsing 
0) Parsing the .txt files with the games (Sequence form games of any leduc 1-to-13)
1) Creating data structures (dataframes) to contain the informations about game: game_nodes.csv, game_infosets.csv
### 01-Clustering 
2) Dimensionality reduction without information loss
3) Clustering the information sets in order to reduce more game dimensionality (Abstract Generation)
### 02-CFR 
4) CFR Learning Algorithm (Vanilla, Monte Carlo) to reach epsilon-Nash equilibrium strategies on abstract game
5) Map abstract strategies to real game
### 03-Subgame Refinement 
6) Identify most valuable subgames inside the full game tree
7) Improve current strategies in them through a second pass of the CFR Algorithm on them
### 04-Strategy Evaluation
8) Calculation of the strategy's exploitability
9) Possibility to play against the bot through a simulator


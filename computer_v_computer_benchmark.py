from TicTacToe import *

winner_history = {-1: {'name': 'computer 1', 'wins': 0},
            1: {'name': 'computer 2', 'wins': 0},
            'tie': {'name': 'nobody', 'wins': 0}
            }

for round in range(10000):

    winner = play_computer_vs_computer()[2]
    winner_history[winner]['wins'] += 1

for key in winner_history.keys():
    print(winner_history[key])

from TicTacToe import *
import json

json_path = 'random_ai_training_data.json'

winner_history = {-1: {'name': 'computer 1', 'wins': 0},
            1: {'name': 'computer 2', 'wins': 0},
            'tie': {'name': 'nobody', 'wins': 0}
            }

all_boards = []
all_moves = []

for round in range(25000):

    new_boards, new_moves = make_data()
    temp_boards = []

    if new_boards:
        temp_boards += new_boards

        for board in temp_boards:
            new_board = []
            for row in board:
                new_board += row
            all_boards += [new_board]

        all_moves += new_moves

data = {'boards': all_boards,
        'moves': all_moves}

with open(json_path, 'w') as outfile:
    json.dump(data, outfile)



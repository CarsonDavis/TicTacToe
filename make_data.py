import TicTacToe
import json

# json_path = 'Models and Data/Loss Training/Smart_Loses_to_Random.json'

winner_history = {1: {'name': 'player 1', 'wins': 0},
                  -1: {'name': 'player 2', 'wins': 0},
                  'tie': {'name': 'nobody', 'wins': 0}
                  }

all_boards = []
all_moves = []

for game in range(5):

    # new_boards, new_moves, winner = make_data()
    new_boards, new_moves, winner = TicTacToe.play(print_on = False)

    winner_history[winner]['wins'] += 1
    filtered_boards = []
    filtered_moves = []

    # filter out the boards from the loser
    if winner == 1:
        for i in range(len(new_moves)):
            if i % 2 == 0: # takes only boards from player one
                filtered_boards.append(new_boards[i])
                filtered_moves.append(new_moves[i])

    elif winner == -1:
        for i in range(len(new_moves)):
            if i % 2 != 0: # takes only boards from player two
                temp = [num * -1 for num in new_boards[i]]  # boards must be inverted for player 2
                filtered_boards.append(temp)
                filtered_moves.append(new_moves[i])

    # add filtered boards to the data
    if filtered_boards:
        all_boards += filtered_boards
        all_moves += filtered_moves


data = {'boards': all_boards,
        'moves': all_moves}

for player in winner_history.keys():
    print(winner_history[player]['name'], winner_history[player]['wins'])

# with open(json_path, 'w') as outfile:
#     json.dump(data, outfile)


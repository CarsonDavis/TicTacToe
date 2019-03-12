from TicTacToe import play
import json

# json_path = 'Models and Data/Loss Training/Random_Smart_Losses.json'

winner_history = {1: {'name': 'player 1', 'wins': 0},
                  -1: {'name': 'player 2', 'wins': 0},
                  'tie': {'name': 'nobody', 'wins': 0}
                  }

all_boards = []
all_moves = []
wins = 0
for round in range(30):
    print()
    print('ROUND')
    print(round)

    # new_boards, new_moves, winner = make_data()
    all_new_boards, all_new_moves, winner = play(True)

    winner_history[winner]['wins'] += 1

    new_boards = []
    new_moves = []

    if winner == 1:
        for i in range(len(all_new_moves)):
            if i % 2 == 0:
                new_boards.append(all_new_boards[i])
                new_moves.append(all_new_moves[i])
    elif winner == -1 and all_new_boards:
        for i in range(len(all_new_moves)):
            if i % 2 != 0:
                temp = [[num * -1 for num in row] for row in all_new_boards[i]]  # boards must be inverted for player 2
                new_boards.append(temp)
                new_moves.append(all_new_moves[i])

    temp_boards = []

    if new_boards:
        temp_boards += new_boards

        for board in temp_boards:
            new_board = []
            for row in board:
                new_board += row
            all_boards += [new_board]

        all_moves += new_moves

        wins += 1

data = {'boards': all_boards,
        'moves': all_moves}

for player in winner_history.keys():
    print(winner_history[player]['name'], winner_history[player]['wins'])

# with open(json_path, 'w') as outfile:
#     json.dump(data, outfile)

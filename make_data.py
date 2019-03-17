from TicTacToe import Game

def play(model, print_on, probability):
    game = Game(model)
    return game.play(print_on, probability)


# json_path = 'Models and Data/Baseline/all_possible_games.json'
def make_data(model, iterations, probability=1):

    winner_history = {1: {'name': 'player 1', 'wins': 0},
                    -1: {'name': 'player 2', 'wins': 0},
                    'tie': {'name': 'nobody', 'wins': 0}
                    }

    all_boards = []
    all_moves = []

    for game in range(iterations):

        # new_boards, new_moves, winner = make_data()
        new_boards, new_moves, winner = play(model, print_on = False, probability = probability)

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
            print(winner)
            print(new_boards)
            print(new_moves)
            for i in range(len(new_moves)):
                if i % 2 != 0: # takes only boards from player two
                    temp = [num * -1 for num in new_boards[i]]  # boards must be inverted for player 2
                    filtered_boards.append(temp)
                    filtered_moves.append(new_moves[i])

        # add filtered boards to the data
        if filtered_boards:
            all_boards += filtered_boards
            all_moves += filtered_moves


    winning_boards = {'boards': all_boards,
                      'moves': all_moves}

    return winning_boards, winner_history


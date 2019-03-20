from TicTacToe import Game

def play(winning_model, losing_model, print_on, probability):
    game = Game(winning_model, losing_model)
    return game.play(print_on, probability)


# json_path = 'Models and Data/Baseline/all_possible_games.json'
def make_data(winning_model, losing_model, iterations, probability=1):

    winner_history = {1: {'name': 'player 1', 'wins': 0},
                    -1: {'name': 'player 2', 'wins': 0},
                    'tie': {'name': 'nobody', 'wins': 0}
                    }

    all_winning_boards = []
    all_winning_moves = []

    all_losing_boards = []
    all_losing_moves = []

    for game in range(iterations):

        # new_boards, new_moves, winner = make_data()
        new_boards, new_moves, winner = play(winning_model, losing_model, print_on = False, probability = probability)

        winner_history[winner]['wins'] += 1
        winning_boards = []
        winning_moves = []

        losing_boards = []
        losing_moves = []

        # filter out the boards from the loser
        if winner == 1:
            for i in range(len(new_moves)):
                if i % 2 == 0:  # takes only boards from player one
                    winning_boards.append(new_boards[i])
                    winning_moves.append(new_moves[i])
                else:  # takes only boards from player two
                    losing_boards.append(new_boards[i])
                    losing_moves.append(new_moves[i])                   

        elif winner == -1:
            for i in range(len(new_moves)):
                temp = [num * -1 for num in new_boards[i]]  # boards must be inverted for player 2
                if i % 2 != 0:  # takes only boards from player two
                    winning_boards.append(temp)
                    winning_moves.append(new_moves[i])
                else:  # takes only boards from player one
                    losing_boards.append(temp)
                    losing_moves.append(new_moves[i])                    

        # add winning boards to the data
        if winning_boards:
            all_winning_boards += winning_boards
            all_winning_moves += winning_moves

            all_losing_boards += losing_boards
            all_losing_moves += losing_moves


    winning_data = {'boards': all_winning_boards,
                      'moves': all_winning_moves}

    losing_data = {'boards': all_losing_boards,
                    'moves': all_losing_moves}

    return winning_data, losing_data, winner_history


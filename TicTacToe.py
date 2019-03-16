from random import choice
from keras.models import load_model
import numpy as np
model = load_model('Models and Data/Smart Training/smart_model.h5')
# old_model = load_model('Models and Data/Random Training/random_model.h5')

# TODO: think about tracking the current player instead of passing around the player to every function
# TODO: integrate the play function into the class


class Game:
    def __init__(self):
        self.current_board = [0, 0, 0,
                              0, 0, 0,
                              0, 0, 0]

        self.board_history = list()
        self.move_history = list()
        self.valid_moves = set(range(9))
        self.game_over = False
        self.winner = None

    def move(self, position, player):

        # update board and move history
        self.board_history.append(self.current_board.copy())
        self.move_history.append(position)

        # remove move from total possible moves
        self.valid_moves.remove(position)

        # make the move by updating the current board
        self.current_board[position] = player

        # update the game over variable
        self.game_over = self.is_victory(self.current_board)

        # print('Player', player, 'moved', position)
        # print()

    def is_victory(self, board):

        # rows
        if abs(board[0]+board[1]+board[2]) == 3: return True
        if abs(board[3]+board[4]+board[5]) == 3: return True
        if abs(board[6]+board[7]+board[8]) == 3: return True 

        # cols
        if abs(board[0]+board[3]+board[6]) == 3: return True
        if abs(board[1]+board[4]+board[7]) == 3: return True
        if abs(board[2]+board[5]+board[8]) == 3: return True

        # across
        if abs(board[0]+board[4]+board[8]) == 3: return True
        if abs(board[2]+board[4]+board[6]) == 3: return True

        return False

    def print_board(self, board):

        print(board[0], board[1], board[2])
        print(board[3], board[4], board[5])
        print(board[6], board[7], board[8]) 

    def board_to_vector(self, board, player):

        # reverse board if player 2
        if player == -1:
            board = [num * -1 for num in board]

        return np.array([board])

    def random_move(self, player):
        return choice(list(self.valid_moves)), player

    def smart_move(self, player):

        # turn the board into a vector that can be consumed by the model
        board_vector = self.board_to_vector(self.current_board, player)

        # run the board through the model and generated predictions
        prediction_list = list(model.predict(board_vector)[0])

        while sum(prediction_list):
            # take the move with the highest predicted value then remove it from the prediction list
            move = prediction_list.index(max(prediction_list))
            prediction_list[move] = 0

            # make sure the move predicted by the model is actually available
            if move in self.valid_moves:
                return move, player

        # this is only executed if there are no non-negative predictions left
        return choice(list(self.valid_moves)), player

    def player_move(self, player):

        try:
            move = int(input())
        except ValueError:
            move = None

        while move not in self.valid_moves:
            print('Please choose a valid move from', self.valid_moves)
            move = int(input())

        return move, player


def play(print_on=True):
    # change the functions in the turn map if you want to modify who plays who
    game = Game()

    turn_map = {1: {'name': 'Player 1', 'move function': game.random_move},
                -1: {'name': 'Player 2', 'move function': game.random_move},
                }

    whose_move = 1

    while not game.game_over:

        if not game.valid_moves:
            game.winner = 'tie'
            break

        if print_on:
            print(turn_map[whose_move]['name'] + "'s Move")
            game.print_board(game.current_board)
            print()

        game.move(*turn_map[whose_move]['move function'](whose_move))
        whose_move *= -1

    if game.winner != 'tie':
        game.winner = whose_move * -1

    # if game.winner == 'tie' or game.winner == 1:
    #     game.board_history = None
    #     game.move_history = None

    if print_on:
        game.print_board(game.current_board)
        print()
        if game.winner == 'tie':
            print('There was a tie!')
        else:
            print(turn_map[(whose_move * -1)]['name'], ' wins!')

    return game.board_history, game.move_history, game.winner

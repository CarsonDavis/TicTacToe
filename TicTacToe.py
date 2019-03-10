from random import choice
from keras.models import load_model
import numpy as np
model = load_model('random_model.h5')


class Game:
    def __init__(self, player_piece=1):
        self.current_board = [[0, 0, 0],
                              [0, 0, 0],
                              [0, 0, 0]]
        self.board_history = list()
        self.move_history = list()

        self.valid_moves = set(range(9))
        self.player_piece = player_piece
        self.computer_piece = -1 if player_piece == 1 else 1
        self.game_over = False
        self.winner = None

    def move(self, position, piece=None):
        # position is int 0-8
        # piece is {'O':-1, 'X':1}
        # will accept invalid moves, error handling needs to be somewhere else

        # I am only training player 1 to win, and will therefor only record 1's moves
        if piece == 1:
            # so this ridiculous bit is necessary because otherwise python will use references on the internal lists
            self.board_history += [[[j for j in i] for i in self.current_board]]
            self.move_history.append(position)

        if not piece:
            piece = self.player_piece

        position = int(position)

        self.valid_moves.remove(position)
        self.current_board[position // 3][position % 3] = piece
        self.game_over = self.is_victory()

    def is_victory(self, board=None):

        if not board:
            board = self.current_board

        # rows
        for row in board:
            if sum(row) == 3 or sum(row) == -3:
                return True

        # columns
        for col in range(3):
            total = 0
            for row in range(3):
                total += board[row][col]
            if total == 3 or total == -3:
                return True

        # across
        total = board[0][0] + board[1][1] + board[2][2]
        if total == 3 or total == -3:
            return True

        total = board[0][2] + board[1][1] + board[2][0]
        if total == 3 or total == -3:
            return True

        return False

    def print_board(self, board=None):
        if not board:
            board = self.current_board

        for row in range(3):
            print(board[row])

    def board_to_prediction_list(self, board=None):
        if not board:
            board = self.current_board

        vector_board = []
        for row in board:
            vector_board += row
        np_board = np.array([vector_board])

        return list(model.predict(np_board)[0])

    def computer_move(self, piece=None):

        if not piece:
            piece = self.computer_piece

        if not self.valid_moves:
            print('aaaahhhh')

        return choice(list(self.valid_moves)), piece

    def smart_move(self, piece=None):

        if not piece:
            piece = self.computer_piece

        prediction_list = self.board_to_prediction_list()

        while True:
            move = prediction_list.index(max(prediction_list))
            prediction_list[move] = 0

            if move in self.valid_moves:
                return move, piece


def play_human_vs_computer():
    game = Game()

    turn_map = {-1: {'name': 'computer', 'move function': game.computer_move},
                1: {'name': 'player', 'move function': input}
                }

    whose_move = 1

    print('Your Move')
    game.print_board()

    while not game.game_over:

        if not game.valid_moves:
            print('there was a tie')
            break

        game.move(*turn_map[whose_move]['move function']())

        print(turn_map[whose_move]['name'] + "'s move")
        game.print_board()
        print()
        whose_move *= -1

    print(turn_map[(whose_move * -1)]['name'], ' wins!')

def play_computer_vs_computer():
    game = Game()

    turn_map = {-1: {'name': 'computer 1', 'move function': game.computer_move},
                1: {'name': 'computer 2', 'move function': game.computer_move},
                'tie': {'name': 'nobody'}
                }

    whose_move = 1

    print('Your Move')
    game.print_board()

    while not game.game_over:

        if not game.valid_moves:
            print('there was a tie')
            game.winner = 'tie'
            break

        game.move(*turn_map[whose_move]['move function'](whose_move))

        print(turn_map[whose_move]['name'] + "'s move")
        game.print_board()
        print()
        whose_move *= -1

    if not game.winner:
        game.winner = whose_move * -1

    print(turn_map[game.winner]['name'], ' wins!')

    return game.board_history, game.move_history, game.winner


def make_data():
    game = Game()

    turn_map = {-1: {'name': 'computer 1', 'move function': game.smart_move},
                1: {'name': 'computer 2', 'move function': game.computer_move},
                'tie': {'name': 'nobody'}
                }

    whose_move = 1

    while not game.game_over:

        if not game.valid_moves:
            game.winner = 'tie'
            break

        game.move(*turn_map[whose_move]['move function'](whose_move))
        whose_move *= -1

    if not game.winner:
        game.winner = whose_move * -1

    if game.winner == 1:
        return game.board_history, game.move_history
    else:
        return None, None


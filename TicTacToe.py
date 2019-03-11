from random import choice
from keras.models import load_model
import numpy as np
model = load_model('Models and Data/Loss Training/loss_model.h5')
old_model = load_model('Models and Data/Random Training/random_model.h5')

# TODO: think about tracking the current player instead of passing around piece to every function
# TODO: integrate the play function into the class
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

    def move(self, position, piece):
      
        # update board and move history
        # so this ridiculous bit is necessary because otherwise python will use references on the internal lists
        self.board_history += [[[j for j in i] for i in self.current_board]]
        self.move_history.append(position)

        # remove move from total possible moves
        self.valid_moves.remove(position)

        # make the move by updating the current board
        self.current_board[position // 3][position % 3] = piece
        
        # update the game over variable
        self.game_over = self.is_victory(self.current_board)

    def is_victory(self, board):

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

    def print_board(self, board):
        for row in range(3):
            print(board[row])

    def board_to_vector(self, board, piece):

        # reverse board if player 2
        if piece == -1:
            board = [[num * -1 for num in row] for row in board]

        # turn board into vector consumable by model
        vector_board = []
        for row in board:
            vector_board += row
        np_board = np.array([vector_board])

        return np_board

    def random_move(self, piece):
        return choice(list(self.valid_moves)), piece

    def smart_move(self, piece):
        
        # turn the board into a vector that can be consumed by the model
        board_vector = self.board_to_vector(self.current_board, piece)

        # run the board through the model and generated predictions
        prediction_list = list(model.predict(board_vector)[0])

        while True:
            # take the move with the highest predicted value then remove it from the prediction list
            move = prediction_list.index(max(prediction_list))
            prediction_list[move] = 0
            
            # make sure the move predicted by the model is actually available
            if move in self.valid_moves:
                return move, piece
 
    # def old_model(self, piece):
        
    #     # turn the board into a vector that can be consumed by the model
    #     board_vector = self.board_to_vector(self.current_board, piece)

    #     # run the board through the model and generated predictions
    #     prediction_list = list(old_model.predict(board_vector)[0])

    #     while True:
    #         # take the move with the highest predicted value then remove it from the prediction list
    #         move = prediction_list.index(max(prediction_list))
    #         prediction_list[move] = 0
            
    #         # make sure the move predicted by the model is actually available
    #         if move in self.valid_moves:
    #             return move, piece

    def player_move(self, piece):
        
        try:
            move = int(input())
        except ValueError:
            move = None

        while move not in self.valid_moves:
            print('Please choose a valid move from', self.valid_moves)
            move = int(input())

        return move, piece

def play(print_on=True):
    # change the functions in the turn map if you want to modify who plays who
    game = Game()

    turn_map = {1: {'name': 'Player 1', 'move function': game.random_move},
               -1: {'name': 'Player 2', 'move function': game.smart_move},
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

    if game.winner == 'tie':
        game.board_history = None
        game.move_history = None
    
    if print_on:
        game.print_board(game.current_board)
        print()
        if game.winner == 'tie':
            print('There was a tie!')
        else:
            print(turn_map[(whose_move * -1)]['name'], ' wins!')       

    return game.board_history, game.move_history, game.winner

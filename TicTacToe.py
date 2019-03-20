from random import choice, choices
from keras.models import load_model
import numpy as np
# model = load_model('Models and Data/Baseline/all_possible_games_3462.h5')
# model = load_model('Models and Data/Baseline/all_possible_games_3.h5')
# old_model = load_model('Models and Data/Random Training/random_model.h5')

# TODO: think about tracking the current player instead of passing around the player to every function
# TODO: integrate the play function into the class


class Game:
    def __init__(self, winning_model, losing_model):
        self.winning_model = winning_model
        self.losing_model = losing_model
        self.current_board = [0, 0, 0,
                              0, 0, 0,
                              0, 0, 0]

        self.board_history = list()
        self.move_history = list()
        self.valid_moves = set(range(9))
        self.game_over = False
        self.winner = None
        self.whose_move = 1

    def move(self, position):
  
        # print(self.whose_move, 'moved', position)
        # print()

        # update board and move history
        self.board_history.append(self.current_board.copy())
        self.move_history.append(position)

        # remove move from total possible moves
        self.valid_moves.remove(position)

        # make the move by updating the current board
        self.current_board[position] = self.whose_move

        # update the game over variable
        self.game_over = self.is_victory(self.current_board)

        # update whose move (this needs to be the absolute last thing)
        self.whose_move *= -1

    def is_victory(self, board):

        over = False

        # rows
        if abs(board[0]+board[1]+board[2]) == 3: over = True
        elif abs(board[3]+board[4]+board[5]) == 3: over = True
        elif abs(board[6]+board[7]+board[8]) == 3: over = True 

        # cols
        elif abs(board[0]+board[3]+board[6]) == 3: over = True
        elif abs(board[1]+board[4]+board[7]) == 3: over = True
        elif abs(board[2]+board[5]+board[8]) == 3: over = True

        # across
        elif abs(board[0]+board[4]+board[8]) == 3: over = True
        elif abs(board[2]+board[4]+board[6]) == 3: over = True


        if over == True:
            self.winner = self.whose_move
        elif not self.valid_moves:
            self.winner = 'tie'
            over = True
            
        return over

    def print_board(self, board):

        print(board[0], board[1], board[2])
        print(board[3], board[4], board[5])
        print(board[6], board[7], board[8]) 

    def board_to_vector(self, board):

        # reverse board if player 2
        if self.whose_move == -1:
            board = [num * -1 for num in board]

        return np.array([board])

    def random_move(self):
        return choice(list(self.valid_moves))

    def smart_move(self):

        # turn the board into a vector that can be consumed by the model
        board_vector = self.board_to_vector(self.current_board)

        # run the board through the model and generated predictions
        prediction_list = list(self.winning_model.predict(board_vector)[0])

        while sum(prediction_list):
            # take the move with the highest predicted value then remove it from the prediction list
            move = prediction_list.index(max(prediction_list))
            prediction_list[move] = 0

            # make sure the move predicted by the model is actually available
            if move in self.valid_moves:
                return move

        # this is only executed if there are no non-negative predictions left
        return choice(list(self.valid_moves))

    def player_move(self):

        try:
            move = int(input())
        except ValueError:
            move = None

        while move not in self.valid_moves:
            print('Please choose a valid move from', self.valid_moves)
            move = int(input())

        return move
    
    def randomizer(self, func_1, func_2, probability):
        if probability < 0 or probability > 1:
            raise ValueError
        return choices([func_1, func_2], [probability, 1-probability], k=1)[0]


    def play(self, print_on=True, probability = 1):
        # change the functions in the turn map if you want to modify who plays who

        turn_map = {1: {'name': 'Player 1', 'move function': self.smart_move},
                    -1: {'name': 'Player 2', 'move function': self.random_move},
                    }

        self.whose_move = 1

        while not self.game_over:

            if print_on:
                print(turn_map[self.whose_move]['name'] + "'s Move")
                self.print_board(self.current_board)
                print()

            move_function = self.randomizer(turn_map[self.whose_move]['move function'], self.random_move, probability)
            self.move(move_function())

        if print_on:
            self.print_board(self.current_board)
            print()
            if self.winner == 'tie':
                print('There was a tie!')
            else:
                print(turn_map[(self.whose_move * -1)]['name'], ' wins!')

        return self.board_history, self.move_history, self.winner

from random import choice


class Game():
    def __init__(self, player_piece=1):
        self.current_board = [[0, 0, 0],
                              [0, 0, 0],
                              [0, 0, 0]]
        self.history = list()
        self.valid_moves = set(range(9))
        self.player_piece = player_piece
        self.computer_piece = -1 if player_piece == 1 else 1
        self.game_over = False

    def move(self, position, piece=None):
        # position is int 0-8
        # piece is {'O':-1, 'X':1}
        # will accept invalid moves, error handling needs to be somewhere else

        if not piece: piece = self.player_piece

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

    def computer_move(self):
        return choice(list(self.valid_moves)), self.computer_piece

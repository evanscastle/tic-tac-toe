import numpy as np

BOARD_ROWS = 3
BOARD_COLS = 3

class Board:
    def __init__(self, p1, p2):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.boardHash = None
        self.p1 = p1
        self.p2 = p2

        self.coin_flip = None
        # The player who begins the game is always 'X' regardless of which agent that is. The identity of the winner
        # should not be determined by which symbol wins, but rather which player was using that symbol
        self.starting_player = None
        self.other_player = None

        self.turns_taken = 0

        self.finished = False
        self.winner = None

    def determine_starting_player(self):
        # randomly decide which player goes first
        self.coin_flip = np.random.choice(2)
        if self.coin_flip == 0:
            self.starting_player = 'p1'
            self.other_player = 'p2'

        else:
            self.starting_player = 'p2'
            self.other_player = 'p1'

    def getHash(self):
        self.boardHash = str(self.board.reshape(BOARD_ROWS*BOARD_COLS))
        return self.boardHash

    def getMoves(self):
        moves = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i][j] == 0:
                    moves.append((i, j))

        return moves

    def makeMove(self, move):
        if self.board[move[0]][move[1]] != 0:
            raise ValueError('Board Space is not Empty')

        else:
            # first player is always the X player
            if self.turns_taken % 2 == 0:
                self.board[move[0]][move[1]] = 1
            else:
                self.board[move[0]][move[1]] = -1

            self.turns_taken += 1


    def isFinished(self):
        # check rows for a winner
        for i in range(BOARD_ROWS):
            if sum(self.board[i, :]) == 3:
                self.finished = True
                self.winner = self.starting_player
                return self.finished

            if sum(self.board[i, :]) == -3:
                self.finished = True
                self.winner = self.other_player
                return self.finished

        # check cols for a winner
        for j in range(BOARD_COLS):
            if sum(self.board[:, j]) == 3:
                self.finished = True
                self.winner = self.starting_player
                return self.finished

            if sum(self.board[:, j]) == -3:
                self.finished = True
                self.winner = self.other_player
                return self.finished

        # check diagonals for a winner
        if (self.board[0, 0] + self.board[1, 1] + self.board[2, 2] == 3) or (self.board[2, 0] + self.board[1, 1] + self.board[0, 2] == 3):
            self.finished = True
            self.winner = self.starting_player
            return self.finished

        if (self.board[0, 0] + self.board[1, 1] + self.board[2, 2] == -3) or (self.board[2, 0] + self.board[1, 1] + self.board[0, 2] == -3):
            self.finished = True
            self.winner = self.other_player
            return self.finished

        moves = self.getMoves()
        if len(moves) == 0:
            self.finished = True
            return self.finished

    def print(self):
        symbols = {1: 'X', -1: 'O', 0: '_'}

        for i in range(BOARD_ROWS):
            line = ''
            for j in range(BOARD_COLS):
                line = line + symbols[self.board[i, j]] + ' '
            print(line)
        print()


    def copy(self):
        board_copy = Board(self.p1, self.p2)
        board_copy.board = self.board.copy()

        board_copy.boardHash = None
        board_copy.turns_taken = self.turns_taken

        board_copy.finished = self.finished
        board_copy.winner = self.winner

        return board_copy


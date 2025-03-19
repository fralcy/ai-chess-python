from logic.player import Player
from logic.pieces import *
from logic.position import Position

class Board:
    def __init__(self):
        self._pieces = [[None for _ in range(8)] for _ in range(8)]
        self.add_starting_pieces()

    def get_piece(self, key):
        if isinstance(key, tuple):
            row, col = key
            return self._pieces[row][col]
        else:
            return self._pieces[key.row][key.column]
        
    def set_piece(self, key, value):
        if isinstance(key, tuple):
            row, col = key
            self._pieces[row][col] = value
        else:
            self._pieces[key.row][key.column] = value

    def add_starting_pieces(self):
        # Add black pieces
        self._pieces[0][0] = Rook(Player.BLACK)
        self._pieces[0][1] = Knight(Player.BLACK)
        self._pieces[0][2] = Bishop(Player.BLACK)
        self._pieces[0][3] = Queen(Player.BLACK)
        self._pieces[0][4] = King(Player.BLACK)
        self._pieces[0][5] = Bishop(Player.BLACK)
        self._pieces[0][6] = Knight(Player.BLACK)
        self._pieces[0][7] = Rook(Player.BLACK)
        # Add white pieces
        self._pieces[7][0] = Rook(Player.WHITE)
        self._pieces[7][1] = Knight(Player.WHITE)
        self._pieces[7][2] = Bishop(Player.WHITE)
        self._pieces[7][3] = Queen(Player.WHITE)
        self._pieces[7][4] = King(Player.WHITE)
        self._pieces[7][5] = Bishop(Player.WHITE)
        self._pieces[7][6] = Knight(Player.WHITE)
        self._pieces[7][7] = Rook(Player.WHITE)
        # Add pawns
        for i in range(8):
            self._pieces[1][i] = Pawn(Player.BLACK)
            self._pieces[6][i] = Pawn(Player.WHITE)
        return self._pieces
    
    def is_inside(self, pos: Position):
        return 0 <= pos.row < 8 and 0 <= pos.column < 8
    
    def is_empty(self, pos: Position):
        return self.get_piece(pos) is None
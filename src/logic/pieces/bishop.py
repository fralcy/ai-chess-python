from piece import Piece
from piece_type import PieceType
from player import Player

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)

    @property
    def piece_type(self):
        return PieceType.BISHOP

    def copy(self):
        copy = Bishop(self.color)
        copy.has_moved = self.has_moved
        return copy
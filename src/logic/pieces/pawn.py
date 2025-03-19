from piece import Piece
from piece_type import PieceType
from player import Player

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)

    @property
    def piece_type(self):
        return PieceType.PAWN

    def copy(self):
        copy = Pawn(self.color)
        copy.has_moved = self.has_moved
        return copy
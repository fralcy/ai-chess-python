from piece import Piece
from piece_type import PieceType
from player import Player

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)

    @property
    def piece_type(self):
        return PieceType.ROOK
    
    def copy(self):
        copy = Rook(self.color)
        copy.has_moved = self.has_moved
        return copy
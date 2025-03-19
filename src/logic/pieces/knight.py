from piece import Piece
from piece_type import PieceType
from player import Player

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
    
    @property
    def piece_type(self):
        return PieceType.KNIGHT
    
    def copy(self):
        copy = Knight(self.color)
        copy.has_moved = self.has_moved
        return copy
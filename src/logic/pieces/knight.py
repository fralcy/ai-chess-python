from logic.pieces.piece import Piece
from logic.piece_type import PieceType

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
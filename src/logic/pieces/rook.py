from logic.pieces.piece import Piece
from logic.piece_type import PieceType
from logic.direction import Direction

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
    
    @property
    def directions(self):
        return [Direction.North, Direction.East, Direction.South, Direction.West]
    
    def get_moves(self, from_pos, board):
        for direction in self.directions:
            yield from self.move_positions_in_dir(from_pos, board, direction)
from logic.pieces.piece import Piece
from logic.piece_type import PieceType
from logic.direction import Direction

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
    
    @property
    def directions(self):
        return [Direction.NorthWest, Direction.NorthEast, Direction.SouthWest, Direction.SouthEast]
    
    def get_moves(self, from_pos, board):
        for direction in self.directions:
            yield from self.move_positions_in_dir(from_pos, board, direction)
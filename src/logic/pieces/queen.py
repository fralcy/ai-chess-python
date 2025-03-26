from logic.pieces.piece import Piece
from logic.piece_type import PieceType
from logic.direction import Direction

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)

    @property
    def piece_type(self):
        return PieceType.QUEEN
    
    def copy(self):
        copy = Queen(self.color)
        copy.has_moved = self.has_moved
        return copy
    
    @property
    def directions(self):
        return [Direction.NORTH, Direction.NORTH_EAST, Direction.EAST, Direction.SOUTH_EAST,
            Direction.SOUTH, Direction.SOUTH_WEST, Direction.WEST, Direction.NORTH_WEST]
    
    def get_moves(self, from_pos, board):
        for direction in self.directions:
            yield from self.move_positions_in_dir(from_pos, board, direction)
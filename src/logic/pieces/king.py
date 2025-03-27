from logic.pieces.piece import Piece
from logic.piece_type import PieceType
from logic.direction import Direction
from logic.moves.normal_move import NormalMove

class King(Piece):
    def __init__(self, color):
        super().__init__(color)

    @property
    def piece_type(self):
        return PieceType.KING
    
    def copy(self):
        copy = King(self.color)
        copy.has_moved = self.has_moved
        return copy
    
    @property
    def directions(self):
        return [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST, 
                Direction.NORTH_WEST, Direction.NORTH_EAST, Direction.SOUTH_WEST, Direction.SOUTH_EAST]
    
    def can_capture_opponent_king(self, from_pos, board):
        for direction in self.directions:
            to_pos = from_pos + direction
            if board.is_inside(to_pos):
                piece = board.get_piece(to_pos)
                if piece and piece.piece_type == PieceType.KING and piece.color != self.color:
                    return True
        return False
    
    def move_positions(self, from_pos, board):
        for direction in self.directions:
            pos = from_pos + direction
            if board.is_inside(pos) and (board.is_empty(pos) or board.get_piece(pos).color != self.color):
                yield pos

    def get_moves(self, from_pos, board):
        for pos in self.move_positions(from_pos, board):
            yield NormalMove(from_pos, pos)
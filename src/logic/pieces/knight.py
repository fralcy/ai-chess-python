from logic.pieces.piece import Piece
from logic.piece_type import PieceType
from logic.direction import Direction
from logic.moves.normal_move import NormalMove

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
    
    def potential_to_positions(from_pos):
        for vertical_dir in [Direction.NORTH, Direction.SOUTH]:
            for horizontal_dir in [Direction.EAST, Direction.WEST]:
                yield from_pos + 2 * vertical_dir + horizontal_dir
                yield from_pos + 2 * horizontal_dir + vertical_dir

    def move_positions(self, from_pos, board):
        for to_pos in self.potential_to_positions(from_pos):
            if board.is_inside(to_pos):
                if board.is_empty(to_pos) or board[to_pos].color != self.color:
                    yield NormalMove(from_pos, to_pos)

    def get_moves(self, from_pos, board):
        for move in self.move_positions(from_pos, board):
            yield NormalMove(from_pos, move.to_pos)
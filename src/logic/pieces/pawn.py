from logic.pieces.piece import Piece
from logic.piece_type import PieceType
from logic.player import Player
from logic.direction import Direction
from logic.moves.normal_move import NormalMove

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
    
    @property
    def forward(self):
        return Direction.NORTH if self.color == Player.WHITE else Direction.SOUTH
    
    def can_move_to(self, pos, board):
        return board.is_inside(pos) and board.is_empty(pos)
    
    def can_capture_at(self, pos, board):
        return board.is_inside(pos) and not board.is_empty(pos) and board.get_piece(pos).color != self.color
    
    def forward_moves(self, from_pos, board):
        one_move_pos = from_pos + self.forward

        if self.can_move_to(one_move_pos, board):
            yield NormalMove(from_pos,one_move_pos)

            two_move_pos = one_move_pos + self.forward
            if not self.has_moved and self.can_move_to(two_move_pos, board):
                yield NormalMove(from_pos, two_move_pos)
        
    def diagonal_moves(self, from_pos, board):
        for direction in [Direction.WEST, Direction.EAST]:
            to_pos = from_pos + self.forward + direction
            if self.can_capture_at(to_pos, board):
                yield NormalMove(from_pos, to_pos)

    def get_moves(self, from_pos, board):
        yield from self.forward_moves(from_pos, board)
        yield from self.diagonal_moves(from_pos, board)
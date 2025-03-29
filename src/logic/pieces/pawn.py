from logic.pieces.piece import Piece
from logic.piece_type import PieceType
from logic.player import Player
from logic.direction import Direction
from logic.moves.normal_move import NormalMove
from logic.moves.pawn_promotion import PawnPromotion
from logic.moves.double_pawn import DoublePawn
from logic.moves.en_passant import EnPassant

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
    
    def can_capture_opponent_king(self, from_pos, board):
        for direction in [Direction.WEST, Direction.EAST]:
            to_pos = from_pos + self.forward + direction
            if board.is_inside(to_pos):
                piece = board.get_piece(to_pos)
                if piece and piece.piece_type == PieceType.KING and piece.color != self.color:
                    return True
        return False
    
    def promotion_moves(self, from_pos, to_pos):
        yield PawnPromotion(from_pos, to_pos, PieceType.QUEEN)
        yield PawnPromotion(from_pos, to_pos, PieceType.ROOK)
        yield PawnPromotion(from_pos, to_pos, PieceType.BISHOP)
        yield PawnPromotion(from_pos, to_pos, PieceType.KNIGHT)
    
    def forward_moves(self, from_pos, board):
        one_move_pos = from_pos + self.forward

        if self.can_move_to(one_move_pos, board):
            if (one_move_pos.row == 0 or one_move_pos.row == 7):
               for promotion in self.promotion_moves(from_pos, one_move_pos):
                   yield promotion 
            else:
                yield NormalMove(from_pos, one_move_pos)

            two_move_pos = one_move_pos + self.forward
            if not self.has_moved and self.can_move_to(two_move_pos, board):
                yield DoublePawn(from_pos, two_move_pos)
        
    def diagonal_moves(self, from_pos, board):
        for direction in [Direction.WEST, Direction.EAST]:
            to_pos = from_pos + self.forward + direction

            pawn_skip_position = board.get_pawn_skip_position(self.color.opponent())
            if pawn_skip_position is not None and to_pos == pawn_skip_position:
                yield EnPassant(from_pos, to_pos)
            elif self.can_capture_at(to_pos, board):
                if (to_pos.row == 0 or to_pos.row == 7):
                    for promotion in self.promotion_moves(from_pos, to_pos):
                        yield promotion 
                else:
                    yield NormalMove(from_pos, to_pos)

    def get_moves(self, from_pos, board):
        yield from self.forward_moves(from_pos, board)
        yield from self.diagonal_moves(from_pos, board)
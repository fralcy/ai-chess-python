from logic.pieces.piece import Piece
from logic.piece_type import PieceType
from logic.direction import Direction
from logic.move_type import MoveType
from logic.moves.normal_move import NormalMove
from logic.moves.castle import Castle

class King(Piece):
    def __init__(self, color):
        super().__init__(color)

    @property
    def piece_type(self):
        return PieceType.KING
    
    @staticmethod
    def is_unmoved_rook(pos, board):
        if board.is_empty(pos):
            return False
        
        piece = board.get_piece(pos)
        return piece.piece_type == PieceType.ROOK and piece.color == board.get_piece(pos).color and not piece.has_moved
    
    @staticmethod
    def all_empty(positions, board):
        for pos in positions:
            if not board.is_empty(pos):
                return False
        return True
    
    def can_castle_ks(self, from_pos, board):
        if self.has_moved:
            return False
        
        rook_pos = from_pos + Direction.EAST * 3
        if not self.is_unmoved_rook(rook_pos, board):
            return False
        
        positions = [from_pos + Direction.EAST, from_pos + Direction.EAST * 2]
        if not self.all_empty(positions, board):
            return False
        
        return True

    def can_castle_qs(self, from_pos, board):
        if self.has_moved:
            return False
        
        rook_pos = from_pos + Direction.WEST * 4
        if not self.is_unmoved_rook(rook_pos, board):
            return False
        
        positions = [from_pos + Direction.WEST, from_pos + Direction.WEST * 2, from_pos + Direction.WEST * 3]
        if not self.all_empty(positions, board):
            return False
        
        return True
    
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

        if self.can_castle_ks(from_pos, board):
            yield Castle(MoveType.CASTLE_KS, from_pos)

        if self.can_castle_qs(from_pos, board):
            yield Castle(MoveType.CASTLE_QS, from_pos)
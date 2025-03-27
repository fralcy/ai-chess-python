from abc import ABC, abstractmethod
from logic.moves.move import Move
from logic.moves.normal_move import NormalMove
from logic.piece_type import PieceType
from typing import List

class Piece(ABC):
    def __init__(self, color):
        self._color = color
        self._has_moved = False

    @property
    @abstractmethod
    def piece_type(self):
        pass
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
    
    @property
    def has_moved(self):
        return self._has_moved
    
    @has_moved.setter
    def has_moved(self, value):
        self._has_moved = value

    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def get_moves(self, from_pos, board) -> List["Move"]:
        pass
    
    def can_capture_opponent_king(self, from_pos, board):
        for move in self.get_moves(from_pos, board):
            to_piece = board.get_piece(move.to_pos)
            if to_piece and to_piece.piece_type == PieceType.KING and to_piece.color != self.color:
                return True
        return False

    def move_positions_in_dir(self, from_pos, board, direction):
        pos = from_pos + direction
        while board.is_inside(pos):
            if board.is_empty(pos):
                yield NormalMove(from_pos, pos)
            else:
                piece = board.get_piece(pos)
                if piece.color != self.color:
                    yield NormalMove(from_pos, pos)
                break
            pos += direction 

    def move_positions_in_dirs(self, from_pos, board, directions):
        for direction in directions:
            yield from self.move_positions_in_dir(from_pos, board, direction)
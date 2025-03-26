from abc import ABC, abstractmethod
from src.logic.moves.move import Move
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

    def move_positions_in_dir(self, from_pos, board, direction):
        pos = from_pos + direction
        while board.is_inside(pos):
            if board.is_empty(pos):
                yield pos
            else:
                piece = board[pos]
                if piece.color != self.color:
                    yield pos
                break
            pos += direction 

    def move_positions_in_dirs(self, from_pos, board, directions):
        for direction in directions:
            yield from self.move_positions_in_dir(from_pos, board, direction)
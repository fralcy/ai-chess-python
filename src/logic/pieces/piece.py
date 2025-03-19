from abc import ABC, abstractmethod
from src.logic.player import Player
from src.logic.piece_type import PieceType

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
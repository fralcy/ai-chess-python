from abc import ABC, abstractmethod

class Move(ABC):
    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def from_pos(self):
        pass

    @property
    @abstractmethod
    def to_pos(self):
        pass

    @abstractmethod
    def execute(self, board):
        pass

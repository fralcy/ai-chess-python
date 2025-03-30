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
    def execute(self, board) -> bool:
        pass
    
    def is_legal(self, board):
        # Get the player color from the piece at the from_pos
        player = board.get_piece(self.from_pos).color

        # Make a copy of the board to simulate the move
        board_copy = board.copy()
        
        # Execute the move on the copy
        self.execute(board_copy)
        
        # Check if the player is in check after the move
        return not board_copy.is_in_check(player)
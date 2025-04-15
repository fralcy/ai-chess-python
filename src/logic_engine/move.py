"""
Move class for chess game.
Represents a move with source and destination positions and type.
"""

from src.logic_engine.position import Position
from src.logic_engine.move_type import MoveType


class Move:
    """
    Represents a move in a chess game.
    """
    
    def __init__(self, from_pos, to_pos, move_type=MoveType.NORMAL, promotion_type=None):
        """
        Initialize a move.
        
        Args:
            from_pos: The starting position (Position object)
            to_pos: The destination position (Position object)
            move_type: The type of move (MoveType enum)
            promotion_type: The type to promote to (for pawn promotion moves)
        """
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.type = move_type
        self.promotion_type = promotion_type
    
    def __str__(self):
        """String representation of the move."""
        type_str = self.type.name.lower() if self.type != MoveType.NORMAL else ""
        promotion_str = f" to {self.promotion_type.name.lower()}" if self.promotion_type else ""
        return f"Move from {self.from_pos} to {self.to_pos} ({type_str}{promotion_str})"
    
    def __repr__(self):
        """Machine readable representation of the move."""
        return f"Move({self.from_pos}, {self.to_pos}, {self.type}, {self.promotion_type})"
    
    def __eq__(self, other):
        """Check if two moves are equal."""
        if not isinstance(other, Move):
            return False
        return (self.from_pos == other.from_pos and 
                self.to_pos == other.to_pos and 
                self.type == other.type and 
                self.promotion_type == other.promotion_type)
    
    def __hash__(self):
        """Hash value for the move."""
        return hash((self.from_pos, self.to_pos, self.type, self.promotion_type))
    
    def copy(self):
        """Create a copy of the move."""
        return Move(self.from_pos, self.to_pos, self.type, self.promotion_type)
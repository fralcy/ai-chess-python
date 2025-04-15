"""
Piece class for chess game.
Represents a chess piece with its type, color, and state.
"""

from src.logic_engine.piece_type import PieceType
from src.logic_engine.player import Player


class Piece:
    """
    Represents a chess piece.
    """
    
    def __init__(self, piece_type, color):
        """
        Initialize a chess piece.
        
        Args:
            piece_type: The type of the piece (PieceType enum)
            color: The color of the piece (Player enum)
        """
        self.piece_type = piece_type
        self.color = color
        self.has_moved = False
    
    def __str__(self):
        """String representation of the piece."""
        color_str = "White" if self.color == Player.WHITE else "Black"
        type_str = self.piece_type.name.capitalize()
        return f"{color_str} {type_str}"
    
    def __repr__(self):
        """Machine readable representation of the piece."""
        return f"Piece({self.piece_type}, {self.color})"
    
    def copy(self):
        """Create a copy of the piece."""
        new_piece = Piece(self.piece_type, self.color)
        new_piece.has_moved = self.has_moved
        return new_piece
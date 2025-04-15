"""
Result class for chess game.
Represents the result of a chess game.
"""

from src.logic_engine.player import Player
from src.logic_engine.end_reason import EndReason


class Result:
    """
    Represents the result of a chess game.
    """
    
    def __init__(self, winner, end_reason):
        """
        Initialize a game result.
        
        Args:
            winner: The winner of the game (Player enum, or Player.NONE for draw)
            end_reason: The reason the game ended (EndReason enum)
        """
        self._winner = winner
        self._end_reason = end_reason
    
    @property
    def winner(self):
        """Get the winner of the game."""
        return self._winner
    
    @property
    def end_reason(self):
        """Get the reason the game ended."""
        return self._end_reason
    
    @staticmethod
    def win(winner):
        """
        Create a win result.
        
        Args:
            winner: The player who won
            
        Returns:
            A Result object
        """
        return Result(winner, EndReason.CHECKMATE)
    
    @staticmethod
    def draw(end_reason):
        """
        Create a draw result.
        
        Args:
            end_reason: The reason for the draw
            
        Returns:
            A Result object
        """
        return Result(Player.NONE, end_reason)
    
    def __str__(self):
        """String representation of the result."""
        if self.winner == Player.NONE:
            return f"Draw by {self.end_reason.name.lower()}"
        return f"{self.winner.name.capitalize()} wins by {self.end_reason.name.lower()}"
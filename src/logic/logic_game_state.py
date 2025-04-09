"""
Logic-based implementation of the game state.
Extends the original GameState class with logic programming capabilities.
"""

from src.logic.game_state import GameState
from src.logic.logic_board import LogicBasedBoard
from src.logic.player import Player
from src.logic_engine.logic_game_state import LogicGameState


class LogicBasedGameState(GameState):
    """
    A game state implementation that uses logic programming under the hood.
    Extends the traditional GameState class but uses logic programming for its operations.
    """
    
    def __init__(self, board=None, current_player=Player.WHITE):
        """
        Initialize the game state.
        
        Args:
            board: A Board object or None to create a new logic-based board
            current_player: The player who goes first
        """
        # Create a logic-based board if none is provided
        if board is None:
            board = LogicBasedBoard()
        
        # Initialize using the traditional way
        super().__init__(board, current_player)
        
        # Create the logic game state
        self.logic_state = LogicGameState(board, current_player)
    
    def legal_moves_for_piece(self, pos):
        """
        Override to use logic representation for getting legal moves.
        
        Args:
            pos: The position of the piece
            
        Returns:
            A list of legal moves
        """
        # Use logic game state to get legal moves
        # This will be fully implemented in Commit 3
        # For now, use the traditional method
        return super().legal_moves_for_piece(pos)
    
    def make_move(self, move):
        """
        Override to use logic representation for making a move.
        
        Args:
            move: The move to make
        """
        # Use logic game state to make the move
        self.logic_state.make_move(move)
        
        # Update the traditional state from the logic state
        board = self.logic_state.to_traditional_board()
        self._board = board
        self._current_player = self.logic_state.current_player
        self._result = self.logic_state.result
        self._no_capture_or_pawn_move = self.logic_state.no_capture_or_pawn_move
        self._state_string = self.logic_state._state_string
        self._state_history = self.logic_state._state_history.copy()
    
    def all_legal_moves_for(self, player):
        """
        Override to use logic representation for getting all legal moves.
        
        Args:
            player: The player to get moves for
            
        Returns:
            A list of legal moves
        """
        # Use logic game state to get all legal moves
        # This will be fully implemented in Commit 3
        # For now, use the traditional method
        return super().all_legal_moves_for(player)
    
    def is_in_check(self, player):
        """
        Override to use logic representation for checking if a player is in check.
        
        Args:
            player: The player to check
            
        Returns:
            True if the player is in check, False otherwise
        """
        # Use logic game state to check if a player is in check
        # This will be fully implemented in Commit 5
        # For now, use the traditional method
        return super().is_in_check(player)
    
    def check_for_game_over(self):
        """
        Override to use logic representation for checking for game over.
        """
        # Use logic game state to check for game over
        self.logic_state.check_for_game_over()
        
        # Update the traditional state
        self._result = self.logic_state.result
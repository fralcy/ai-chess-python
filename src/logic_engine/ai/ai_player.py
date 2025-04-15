"""
AI player using logic programming.
This module provides an AI player that uses the minimax algorithm
with alpha-beta pruning implemented using logic programming.
"""

import sys
import time
import random
from src.logic.player import Player
from src.logic.game_state import GameState
from src.logic.move_type import MoveType
from src.logic.piece_type import PieceType
from src.logic_engine.logic_game_state import LogicGameState
from src.logic_engine.ai.minimax import minimax_logic

class LogicAIPlayer:
    """An AI player using the Minimax algorithm with logic programming."""
    
    def __init__(self, player_color, difficulty=3):
        """
        Initialize the AI player.
        
        Args:
            player_color: Which color the AI plays (Player.WHITE or Player.BLACK)
            difficulty: The depth of the Minimax search (1-5), higher is stronger
        """
        self.player_color = player_color
        self.difficulty = min(max(1, difficulty), 5)  # Clamp difficulty between 1-5
        self.thinking_time = 0.5  # Minimum thinking time in seconds (for UX)
    
    def set_difficulty(self, difficulty):
        """Set the difficulty level (search depth) of the AI."""
        self.difficulty = min(max(1, difficulty), 5)
    
    def choose_move(self, game_state):
        """
        Choose the best move for the AI using the Minimax algorithm.
        
        Args:
            game_state: The current game state
            
        Returns:
            The best move found, or None if there are no legal moves
        """
        if game_state.current_player != self.player_color:
            raise ValueError("Not AI's turn to move")
        
        start_time = time.time()
        
        # Convert to a logic-based game state if needed
        if not isinstance(game_state, LogicGameState):
            logic_game_state = LogicGameState(game_state.board, game_state.current_player)
        else:
            logic_game_state = game_state
        
        # Get legal moves
        legal_moves = logic_game_state.all_legal_moves_for(self.player_color)
        
        if not legal_moves:
            return None
        
        # If only one legal move, return it immediately
        if len(legal_moves) == 1:
            # Ensure minimum thinking time for better UX
            remaining_time = self.thinking_time - (time.time() - start_time)
            if remaining_time > 0:
                time.sleep(remaining_time)
            return legal_moves[0]
        
        # For very low difficulty (level 1), just make a random move
        if self.difficulty == 1:
            best_move = random.choice(legal_moves)
            
            # Ensure minimum thinking time for better UX
            remaining_time = self.thinking_time - (time.time() - start_time)
            if remaining_time > 0:
                time.sleep(remaining_time)
                
            return best_move
        
        # For higher difficulties, use minimax with alpha-beta pruning
        depth = self.difficulty
        
        # Run the minimax search
        _, best_move = minimax_logic(
            logic_game_state, 
            depth, 
            -sys.maxsize, 
            sys.maxsize, 
            self.player_color
        )
        
        # If no move was found (shouldn't happen), choose a random move
        if best_move is None and legal_moves:
            best_move = random.choice(legal_moves)
        
        # Ensure minimum thinking time for better UX
        elapsed_time = time.time() - start_time
        if elapsed_time < self.thinking_time:
            time.sleep(self.thinking_time - elapsed_time)
        
        return best_move
    
    def handle_promotion(self, game_state, from_pos, to_pos):
        """
        Choose the piece type for pawn promotion.
        AI will almost always choose Queen as it's the strongest piece.
        
        Args:
            game_state: The current game state
            from_pos: The position of the pawn
            to_pos: The destination position
            
        Returns:
            The piece type to promote to (usually QUEEN)
        """
        # Almost always choose Queen, as it's the strongest piece
        return PieceType.QUEEN
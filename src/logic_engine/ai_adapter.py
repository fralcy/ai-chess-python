"""
Adapter for connecting the logic-based AI to the game UI.
"""

from src.ai.ai_player import AIPlayer
from src.logic_engine.ai.ai_player import LogicAIPlayer
from src.logic_engine.logic_game_state import LogicGameState

class LogicAIAdapter(AIPlayer):
    """
    Adapter class that provides the same interface as the original AIPlayer
    but uses the logic-based implementation under the hood.
    """
    
    def __init__(self, player_color, difficulty=3):
        """
        Initialize the AI adapter.
        
        Args:
            player_color: Which color the AI plays (Player.WHITE or Player.BLACK)
            difficulty: The depth of the Minimax search (1-5), higher is stronger
        """
        super().__init__(player_color, difficulty)
        
        # Create the logic-based AI player
        self.logic_ai = LogicAIPlayer(player_color, difficulty)
    
    def set_difficulty(self, difficulty):
        """Set the difficulty level (search depth) of the AI."""
        super().set_difficulty(difficulty)
        self.logic_ai.set_difficulty(difficulty)
    
    def choose_move(self, game_state):
        """
        Choose the best move for the AI using the logic-based minimax algorithm.
        
        Args:
            game_state: The current game state
            
        Returns:
            The best move found, or None if there are no legal moves
        """
        # Convert to a logic-based game state
        logic_game_state = LogicGameState(game_state.board, game_state.current_player)
        
        # Use the logic-based AI to choose a move
        return self.logic_ai.choose_move(logic_game_state)
    
    def handle_promotion(self, game_state, from_pos, to_pos):
        """
        Choose the piece type for pawn promotion.
        
        Args:
            game_state: The current game state
            from_pos: The position of the pawn
            to_pos: The destination position
            
        Returns:
            The piece type to promote to
        """
        return self.logic_ai.handle_promotion(game_state, from_pos, to_pos)
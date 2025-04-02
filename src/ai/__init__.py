# Import main AI components for easy access
from src.ai.evaluator import BoardEvaluator
from src.ai.minimax import minimax, minimax_alpha_beta
from src.ai.ai_player import AIPlayer

__all__ = ['BoardEvaluator', 'minimax', 'minimax_alpha_beta', 'AIPlayer']
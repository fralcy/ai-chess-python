"""
AI module for the chess game based on logic programming.
Exports the main components for AI reasoning using logic programming.
"""

from src.logic_engine.ai.minimax import minimax_logic
from src.logic_engine.ai.evaluator import LogicBoardEvaluator
from src.logic_engine.ai.ai_player import LogicAIPlayer

__all__ = [
    'minimax_logic',
    'LogicBoardEvaluator',
    'LogicAIPlayer'
]
"""
Special moves package for the chess logic engine.
Exports the main functions for defining and querying special moves.
"""

from src.logic_engine.special_moves.special_moves import setup_special_moves
from src.logic_engine.special_moves.castling import setup_castling_rules
from src.logic_engine.special_moves.en_passant import setup_en_passant_rules
from src.logic_engine.special_moves.promotion import setup_promotion_rules

__all__ = [
    'setup_special_moves',
    'setup_castling_rules',
    'setup_en_passant_rules',
    'setup_promotion_rules'
]
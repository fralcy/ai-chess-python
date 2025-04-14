"""
Movement rules package for the chess logic engine.
Exports the main functions for defining and querying piece movement.
"""

from src.logic_engine.movement_rules.movement_rules import setup_movement_rules, can_move_query
from src.logic_engine.movement_rules.blocking_rules import setup_blocking_rules
from src.logic_engine.movement_rules.pawn_rules import setup_pawn_rules
from src.logic_engine.movement_rules.knight_rules import setup_knight_rules
from src.logic_engine.movement_rules.bishop_rules import setup_bishop_rules
from src.logic_engine.movement_rules.rook_rules import setup_rook_rules
from src.logic_engine.movement_rules.queen_rules import setup_queen_rules
from src.logic_engine.movement_rules.king_rules import setup_king_rules

__all__ = [
    'setup_movement_rules',
    'can_move_query',
    'setup_blocking_rules',
    'setup_pawn_rules',
    'setup_knight_rules',
    'setup_bishop_rules',
    'setup_rook_rules',
    'setup_queen_rules',
    'setup_king_rules'
]
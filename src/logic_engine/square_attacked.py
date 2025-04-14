"""
Logic for determining if a square is under attack.
"""

from src.logic.piece_type import PieceType
from src.logic.player import Player
from src.logic_engine.predicates import ChessPredicates


def setup_square_attacked_predicate(logic_engine):
    """
    Setup logic for determining if a square is under attack.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    var_attacker = logic_engine.variable("Attacker")
    var_defender = logic_engine.variable("Defender")
    var_piece_type = logic_engine.variable("PieceType")
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    
    # A square is attacked if a piece of the attacking player can capture there
    head = (ChessPredicates.SQUARE_ATTACKED, 
            (var_attacker, var_to_row, var_to_col))
    
    body = [
        # Find all pieces of the attacking player
        (ChessPredicates.PIECE_AT, 
         (var_piece_type, var_attacker, var_from_row, var_from_col)),
        
        # Check if any of these pieces can capture at the target square
        (ChessPredicates.PIECE_CAPTURE, 
         (var_piece_type, var_attacker, var_from_row, var_from_col, var_to_row, var_to_col))
    ]
    
    logic_engine.add_rule(head, body)


def is_square_attacked(logic_engine, attacker, row, col):
    """
    Check if a square is under attack.
    
    Args:
        logic_engine: The logic engine
        attacker: The player who is attacking
        row: The row of the square
        col: The column of the square
        
    Returns:
        True if the square is under attack, False otherwise
    """
    results = logic_engine.query(
        ChessPredicates.SQUARE_ATTACKED,
        attacker, row, col
    )
    
    return len(results) > 0


def is_king_in_check(logic_engine, player):
    """
    Check if a player's king is in check.
    
    Args:
        logic_engine: The logic engine
        player: The player whose king to check
        
    Returns:
        True if the king is in check, False otherwise
    """
    results = logic_engine.query(
        ChessPredicates.IN_CHECK,
        player
    )
    
    return len(results) > 0
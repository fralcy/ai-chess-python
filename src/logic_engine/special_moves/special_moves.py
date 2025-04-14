"""
Main module for special chess moves.
Defines the functions for setting up special move rules.
"""

from src.logic_engine.special_moves.castling import setup_castling_rules
from src.logic_engine.special_moves.en_passant import setup_en_passant_rules
from src.logic_engine.special_moves.promotion import setup_promotion_rules
from src.logic_engine.predicates import ChessPredicates


def setup_special_moves(logic_engine):
    """
    Setup all special move rules in the logic engine.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Setup castling rules
    setup_castling_rules(logic_engine)
    
    # Setup en passant rules
    setup_en_passant_rules(logic_engine)
    
    # Setup promotion rules
    setup_promotion_rules(logic_engine)
    
    # Setup can_move rules that include special moves
    setup_special_move_rules(logic_engine)


def setup_special_move_rules(logic_engine):
    """
    Setup the can_move rules that include special moves.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    var_type = logic_engine.variable("Type")
    var_player = logic_engine.variable("Player")
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_side = logic_engine.variable("Side")
    var_new_type = logic_engine.variable("NewType")
    
    # Can move rule for castling
    head = (ChessPredicates.CAN_MOVE, 
            (var_type, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        (ChessPredicates.PIECE_AT, 
         (var_type, var_player, var_from_row, var_from_col)),
        (ChessPredicates.CAN_CASTLE, 
         (var_player, var_side, var_from_row, var_from_col, var_to_row, var_to_col))
    ]
    
    logic_engine.add_rule(head, body)
    
    # Can move rule for en passant
    head = (ChessPredicates.CAN_MOVE, 
            (var_type, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        (ChessPredicates.PIECE_AT, 
         (var_type, var_player, var_from_row, var_from_col)),
        (ChessPredicates.CAN_EN_PASSANT, 
         (var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    ]
    
    logic_engine.add_rule(head, body)
    
    # Can move rule for promotion
    head = (ChessPredicates.CAN_MOVE, 
            (var_type, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        (ChessPredicates.PIECE_AT, 
         (var_type, var_player, var_from_row, var_from_col)),
        (ChessPredicates.CAN_PROMOTE, 
         (var_player, var_from_row, var_from_col, var_to_row, var_to_col, var_new_type))
    ]
    
    logic_engine.add_rule(head, body)
"""
Logic for validating moves to prevent leaving king in check.
"""

from src.logic_engine.piece_type import PieceType
from src.logic_engine.player import Player
from src.logic_engine.predicates import ChessPredicates


def setup_move_check_rules(logic_engine):
    """
    Setup rules for validating moves to prevent leaving king in check.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    setup_leaves_in_check_rule(logic_engine)
    setup_resolve_check_rule(logic_engine)
    setup_move_results_in_check_rule(logic_engine)


def setup_leaves_in_check_rule(logic_engine):
    """
    Setup rule to determine if a move would leave the king in check.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    var_player = logic_engine.variable("Player")
    var_piece_type = logic_engine.variable("PieceType")
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    
    # A move leaves the king in check if simulating the move results in check
    head = (ChessPredicates.LEAVES_IN_CHECK, 
            (var_player, var_piece_type, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        (ChessPredicates.MOVE_RESULTS_IN_CHECK, 
         (var_player, var_piece_type, var_from_row, var_from_col, var_to_row, var_to_col))
    ]
    
    logic_engine.add_rule(head, body)


def setup_move_results_in_check_rule(logic_engine):
    """
    Setup rule to simulate a move and check if it results in check.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # This is a meta-level predicate that needs to be implemented
    # in the execution engine rather than as logical rules, since
    # it involves creating a temporary board state, making a move,
    # and checking if the king is in check.
    pass


def setup_resolve_check_rule(logic_engine):
    """
    Setup rule to determine if a move resolves check.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    var_player = logic_engine.variable("Player")
    var_piece_type = logic_engine.variable("PieceType")
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    
    # A move resolves check if the player is in check and the move doesn't leave the king in check
    head = (ChessPredicates.RESOLVES_CHECK, 
            (var_player, var_piece_type, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        (ChessPredicates.IN_CHECK, 
         (var_player)),
        ("not", ((ChessPredicates.LEAVES_IN_CHECK, 
                 (var_player, var_piece_type, var_from_row, var_from_col, var_to_row, var_to_col))))
    ]
    
    logic_engine.add_rule(head, body)


def is_legal_move(logic_engine, player, piece_type, from_row, from_col, to_row, to_col):
    """
    Check if a move is legal (doesn't leave king in check).
    
    Args:
        logic_engine: The logic engine
        player: The player making the move
        piece_type: The type of piece to move
        from_row: The current row of the piece
        from_col: The current column of the piece
        to_row: The target row
        to_col: The target column
        
    Returns:
        True if the move is legal, False otherwise
    """
    # First check if the move is valid according to chess rules
    move_valid_results = logic_engine.query(
        ChessPredicates.CAN_MOVE,
        piece_type, player, from_row, from_col, to_row, to_col
    )
    
    if not move_valid_results:
        return False
    
    # Then check if the move would leave the king in check
    check_results = logic_engine.query(
        ChessPredicates.LEAVES_IN_CHECK,
        player, piece_type, from_row, from_col, to_row, to_col
    )
    
    return len(check_results) == 0
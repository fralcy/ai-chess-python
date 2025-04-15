"""
Logic for determining checkmate and stalemate conditions.
"""

from src.logic_engine.piece_type import PieceType
from src.logic_engine.player import Player
from src.logic_engine.predicates import ChessPredicates


def setup_checkmate_stalemate_rules(logic_engine):
    """
    Setup rules for detecting checkmate and stalemate.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    setup_no_legal_moves_rule(logic_engine)
    setup_checkmate_rule(logic_engine)
    setup_stalemate_rule(logic_engine)


def setup_no_legal_moves_rule(logic_engine):
    """
    Setup rule to determine if a player has no legal moves.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    var_player = logic_engine.variable("Player")
    var_piece_type = logic_engine.variable("PieceType")
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    
    # A player has no legal moves if there are no pieces that can move
    head = (ChessPredicates.NO_LEGAL_MOVES, 
            (var_player))
    
    body = [
        ("not", ((ChessPredicates.HAS_LEGAL_MOVE, 
                 (var_player))))
    ]
    
    logic_engine.add_rule(head, body)
    
    # A player has a legal move if any of their pieces can move
    head = (ChessPredicates.HAS_LEGAL_MOVE, 
            (var_player))
    
    body = [
        # Find any piece belonging to the player
        (ChessPredicates.PIECE_AT, 
         (var_piece_type, var_player, var_from_row, var_from_col)),
        
        # Check if there is any legal move for this piece
        (ChessPredicates.CAN_MOVE, 
         (var_piece_type, var_player, var_from_row, var_from_col, var_to_row, var_to_col)),
        
        # Ensure the move doesn't leave the king in check
        ("not", ((ChessPredicates.LEAVES_IN_CHECK, 
                 (var_player, var_piece_type, var_from_row, var_from_col, var_to_row, var_to_col))))
    ]
    
    logic_engine.add_rule(head, body)


def setup_checkmate_rule(logic_engine):
    """
    Setup rule to determine if a player is in checkmate.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    var_player = logic_engine.variable("Player")
    
    # A player is in checkmate if they are in check and have no legal moves
    head = (ChessPredicates.CHECKMATE, 
            (var_player))
    
    body = [
        (ChessPredicates.IN_CHECK, 
         (var_player)),
        (ChessPredicates.NO_LEGAL_MOVES, 
         (var_player))
    ]
    
    logic_engine.add_rule(head, body)


def setup_stalemate_rule(logic_engine):
    """
    Setup rule to determine if a player is in stalemate.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    var_player = logic_engine.variable("Player")
    
    # A player is in stalemate if they are not in check but have no legal moves
    head = (ChessPredicates.STALEMATE, 
            (var_player))
    
    body = [
        ("not", ((ChessPredicates.IN_CHECK, 
                 (var_player)))),
        (ChessPredicates.NO_LEGAL_MOVES, 
         (var_player))
    ]
    
    logic_engine.add_rule(head, body)


def is_checkmate(logic_engine, player):
    """
    Check if a player is in checkmate.
    
    Args:
        logic_engine: The logic engine
        player: The player to check
        
    Returns:
        True if the player is in checkmate, False otherwise
    """
    results = logic_engine.query(
        ChessPredicates.CHECKMATE,
        player
    )
    
    return len(results) > 0


def is_stalemate(logic_engine, player):
    """
    Check if a player is in stalemate.
    
    Args:
        logic_engine: The logic engine
        player: The player to check
        
    Returns:
        True if the player is in stalemate, False otherwise
    """
    results = logic_engine.query(
        ChessPredicates.STALEMATE,
        player
    )
    
    return len(results) > 0
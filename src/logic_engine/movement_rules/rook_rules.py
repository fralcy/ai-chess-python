"""
Movement rules for rooks.
"""

from src.logic.piece_type import PieceType
from src.logic_engine.predicates import ChessPredicates


def setup_rook_rules(logic_engine):
    """
    Setup movement rules for rooks.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Rooks move horizontally and vertically
    setup_rook_moves(logic_engine)
    
    # Rook capture rules are the same as movement rules
    setup_rook_captures(logic_engine)


def setup_rook_moves(logic_engine):
    """
    Setup horizontal and vertical movement rules for rooks.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Rooks move in four directions:
    # North (decreasing row, same column)
    # South (increasing row, same column)
    # East (same row, increasing column)
    # West (same row, decreasing column)
    
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_player = logic_engine.variable("Player")
    
    # Horizontal movement (East-West)
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.ROOK, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("equal", (var_from_row, var_to_row)),  # Same row (horizontal movement)
        ("not_equal", (var_from_col, var_to_col)),  # Different column
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)
    
    # Vertical movement (North-South)
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.ROOK, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("equal", (var_from_col, var_to_col)),  # Same column (vertical movement)
        ("not_equal", (var_from_row, var_to_row)),  # Different row
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)


def setup_rook_captures(logic_engine):
    """
    Setup capture rules for rooks.
    Rook captures are the same as movement patterns.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_player = logic_engine.variable("Player")
    
    # Horizontal capture (East-West)
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.ROOK, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("equal", (var_from_row, var_to_row)),  # Same row (horizontal movement)
        ("not_equal", (var_from_col, var_to_col)),  # Different column
        # We need to check if the path is clear up to (but not including) the target square
        # This is handled by the IS_BLOCKED predicate which will check all squares between
        # the source and target
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)
    
    # Vertical capture (North-South)
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.ROOK, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("equal", (var_from_col, var_to_col)),  # Same column (vertical movement)
        ("not_equal", (var_from_row, var_to_row)),  # Different row
        # We need to check if the path is clear up to (but not including) the target square
        # This is handled by the IS_BLOCKED predicate which will check all squares between
        # the source and target
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)
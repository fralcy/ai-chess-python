"""
Movement rules for kings.
"""

from src.logic.piece_type import PieceType
from src.logic.player import Player
from src.logic_engine.predicates import ChessPredicates


def setup_king_rules(logic_engine):
    """
    Setup movement rules for kings.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Kings move one square in any direction
    setup_king_basic_moves(logic_engine)
    
    # King capture rules are the same as basic movement rules
    setup_king_captures(logic_engine)
    
    # Castling will be implemented in commit 4 with special moves


def setup_king_basic_moves(logic_engine):
    """
    Setup basic one-square movement rules for kings.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Kings can move one square in 8 directions:
    # North, South, East, West, Northeast, Northwest, Southeast, Southwest
    
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_player = logic_engine.variable("Player")
    var_row_diff = logic_engine.variable("RowDiff")
    var_col_diff = logic_engine.variable("ColDiff")
    
    # General rule for king movement - one square in any direction
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.KING, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        # Calculate absolute row difference
        ("subtract", (var_from_row, var_to_row, var_row_diff)),
        ("abs", (var_row_diff, var_row_diff)),  # Get absolute value
        
        # Calculate absolute column difference
        ("subtract", (var_from_col, var_to_col, var_col_diff)),
        ("abs", (var_col_diff, var_col_diff)),  # Get absolute value
        
        # Maximum of row and column difference must be 1
        ("less_than_or_equal", (var_row_diff, 1)),  # RowDiff <= 1
        ("less_than_or_equal", (var_col_diff, 1)),  # ColDiff <= 1
        
        # At least one of the differences must be non-zero
        ("or", (
            ("greater_than", (var_row_diff, 0)),  # RowDiff > 0
            ("greater_than", (var_col_diff, 0))   # ColDiff > 0
        ))
    ]
    
    logic_engine.add_rule(head, body)


def setup_king_captures(logic_engine):
    """
    Setup capture rules for kings.
    King captures are the same as basic movement patterns.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_player = logic_engine.variable("Player")
    var_row_diff = logic_engine.variable("RowDiff")
    var_col_diff = logic_engine.variable("ColDiff")
    
    # General rule for king capture - one square in any direction
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.KING, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        # Calculate absolute row difference
        ("subtract", (var_from_row, var_to_row, var_row_diff)),
        ("abs", (var_row_diff, var_row_diff)),  # Get absolute value
        
        # Calculate absolute column difference
        ("subtract", (var_from_col, var_to_col, var_col_diff)),
        ("abs", (var_col_diff, var_col_diff)),  # Get absolute value
        
        # Maximum of row and column difference must be 1
        ("less_than_or_equal", (var_row_diff, 1)),  # RowDiff <= 1
        ("less_than_or_equal", (var_col_diff, 1)),  # ColDiff <= 1
        
        # At least one of the differences must be non-zero
        ("or", (
            ("greater_than", (var_row_diff, 0)),  # RowDiff > 0
            ("greater_than", (var_col_diff, 0))   # ColDiff > 0
        ))
    ]
    
    logic_engine.add_rule(head, body)


def is_king_in_check(logic_engine, player, king_row, king_col):
    """
    Check if a king is in check.
    
    Args:
        logic_engine: The logic engine to query
        player: The player whose king is being checked
        king_row: The row of the king
        king_col: The column of the king
        
    Returns:
        True if the king is in check, False otherwise
    """
    # This will be fully implemented in commit 5
    # For now, we'll just use the existing board.is_in_check method
    opponent = player.opponent()
    var_piece_type = logic_engine.variable("PieceType")
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    
    # Query if any opponent piece can capture the king
    results = logic_engine.query(
        ChessPredicates.PIECE_CAPTURE,
        var_piece_type, opponent, var_from_row, var_from_col, king_row, king_col
    )
    
    return len(results) > 0
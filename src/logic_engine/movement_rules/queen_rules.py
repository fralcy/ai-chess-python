"""
Movement rules for queens.
"""

from src.logic.piece_type import PieceType
from src.logic_engine.predicates import ChessPredicates


def setup_queen_rules(logic_engine):
    """
    Setup movement rules for queens.
    Queens combine the movement of rooks and bishops.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Queens move both diagonally (like bishops) and horizontally/vertically (like rooks)
    setup_queen_diagonal_moves(logic_engine)
    setup_queen_straight_moves(logic_engine)
    
    # Queen capture rules are the same as movement rules
    setup_queen_diagonal_captures(logic_engine)
    setup_queen_straight_captures(logic_engine)


def setup_queen_diagonal_moves(logic_engine):
    """
    Setup diagonal movement rules for queens (like bishops).
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Queens move diagonally in four directions (like bishops):
    # Northeast (decreasing row, increasing column)
    # Northwest (decreasing row, decreasing column)
    # Southeast (increasing row, increasing column)
    # Southwest (increasing row, decreasing column)
    
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_player = logic_engine.variable("Player")
    var_delta = logic_engine.variable("Delta")
    
    # Northeast diagonal
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.QUEEN, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        # Calculate the distance (must be equal in both directions for diagonal)
        ("subtract", (var_from_row, var_to_row, var_delta)),  # Delta = FromRow - ToRow
        ("subtract", (var_to_col, var_from_col, var_delta)),  # Delta = ToCol - FromCol (same delta for diagonal)
        ("greater_than", (var_delta, 0)),  # Delta > 0 (moving up and right)
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)
    
    # Northwest diagonal
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.QUEEN, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        # Calculate the distance (must be equal in both directions for diagonal)
        ("subtract", (var_from_row, var_to_row, var_delta)),  # Delta = FromRow - ToRow
        ("subtract", (var_from_col, var_to_col, var_delta)),  # Delta = FromCol - ToCol (same delta for diagonal)
        ("greater_than", (var_delta, 0)),  # Delta > 0 (moving up and left)
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)
    
    # Southeast diagonal
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.QUEEN, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        # Calculate the distance (must be equal in both directions for diagonal)
        ("subtract", (var_to_row, var_from_row, var_delta)),  # Delta = ToRow - FromRow
        ("subtract", (var_to_col, var_from_col, var_delta)),  # Delta = ToCol - FromCol (same delta for diagonal)
        ("greater_than", (var_delta, 0)),  # Delta > 0 (moving down and right)
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)
    
    # Southwest diagonal
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.QUEEN, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        # Calculate the distance (must be equal in both directions for diagonal)
        ("subtract", (var_to_row, var_from_row, var_delta)),  # Delta = ToRow - FromRow
        ("subtract", (var_from_col, var_to_col, var_delta)),  # Delta = FromCol - ToCol (same delta for diagonal)
        ("greater_than", (var_delta, 0)),  # Delta > 0 (moving down and left)
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)


def setup_queen_straight_moves(logic_engine):
    """
    Setup horizontal and vertical movement rules for queens (like rooks).
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Queens move in four straight directions (like rooks):
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
            (PieceType.QUEEN, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("equal", (var_from_row, var_to_row)),  # Same row (horizontal movement)
        ("not_equal", (var_from_col, var_to_col)),  # Different column
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)
    
    # Vertical movement (North-South)
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.QUEEN, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("equal", (var_from_col, var_to_col)),  # Same column (vertical movement)
        ("not_equal", (var_from_row, var_to_row)),  # Different row
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)


def setup_queen_diagonal_captures(logic_engine):
    """
    Setup diagonal capture rules for queens (like bishops).
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_player = logic_engine.variable("Player")
    var_delta = logic_engine.variable("Delta")
    
    # Northeast diagonal capture
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.QUEEN, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        # Calculate the distance (must be equal in both directions for diagonal)
        ("subtract", (var_from_row, var_to_row, var_delta)),  # Delta = FromRow - ToRow
        ("subtract", (var_to_col, var_from_col, var_delta)),  # Delta = ToCol - FromCol (same delta for diagonal)
        ("greater_than", (var_delta, 0)),  # Delta > 0 (moving up and right)
        # Check if the path to the target is clear (excluding the target itself)
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)
    
    # Northwest diagonal capture
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.QUEEN, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        # Calculate the distance (must be equal in both directions for diagonal)
        ("subtract", (var_from_row, var_to_row, var_delta)),  # Delta = FromRow - ToRow
        ("subtract", (var_from_col, var_to_col, var_delta)),  # Delta = FromCol - ToCol (same delta for diagonal)
        ("greater_than", (var_delta, 0)),  # Delta > 0 (moving up and left)
        # Check if the path to the target is clear (excluding the target itself)
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)
    
    # Southeast diagonal capture
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.QUEEN, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        # Calculate the distance (must be equal in both directions for diagonal)
        ("subtract", (var_to_row, var_from_row, var_delta)),  # Delta = ToRow - FromRow
        ("subtract", (var_to_col, var_from_col, var_delta)),  # Delta = ToCol - FromCol (same delta for diagonal)
        ("greater_than", (var_delta, 0)),  # Delta > 0 (moving down and right)
        # Check if the path to the target is clear (excluding the target itself)
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)
    
    # Southwest diagonal capture
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.QUEEN, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        # Calculate the distance (must be equal in both directions for diagonal)
        ("subtract", (var_to_row, var_from_row, var_delta)),  # Delta = ToRow - FromRow
        ("subtract", (var_from_col, var_to_col, var_delta)),  # Delta = FromCol - ToCol (same delta for diagonal)
        ("greater_than", (var_delta, 0)),  # Delta > 0 (moving down and left)
        # Check if the path to the target is clear (excluding the target itself)
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)


def setup_queen_straight_captures(logic_engine):
    """
    Setup horizontal and vertical capture rules for queens (like rooks).
    
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
            (PieceType.QUEEN, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("equal", (var_from_row, var_to_row)),  # Same row (horizontal movement)
        ("not_equal", (var_from_col, var_to_col)),  # Different column
        # Check if the path to the target is clear (excluding the target itself)
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)
    
    # Vertical capture (North-South)
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.QUEEN, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("equal", (var_from_col, var_to_col)),  # Same column (vertical movement)
        ("not_equal", (var_from_row, var_to_row)),  # Different row
        # Check if the path to the target is clear (excluding the target itself)
        ("not", ((ChessPredicates.IS_BLOCKED, 
                  (var_from_row, var_from_col, var_to_row, var_to_col))))  # Path not blocked
    ]
    
    logic_engine.add_rule(head, body)
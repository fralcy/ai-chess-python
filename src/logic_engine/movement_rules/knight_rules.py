"""
Movement rules for knights.
"""

from src.logic_engine.piece_type import PieceType
from src.logic_engine.predicates import ChessPredicates


def setup_knight_rules(logic_engine):
    """
    Setup movement rules for knights.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Setup basic knight movement rules (L-shape)
    setup_knight_moves(logic_engine)
    
    # Knight capture rules are the same as movement rules
    setup_knight_captures(logic_engine)


def setup_knight_moves(logic_engine):
    """
    Setup L-shaped movement rules for knights.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Knight's L-shape movement patterns (8 possible moves)
    # 2 up, 1 right
    # 2 up, 1 left
    # 2 down, 1 right
    # 2 down, 1 left
    # 2 right, 1 up
    # 2 right, 1 down
    # 2 left, 1 up
    # 2 left, 1 down
    
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_player = logic_engine.variable("Player")
    
    # 2 up, 1 right
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_from_row, 2, var_to_row)),  # ToRow = FromRow - 2
        ("add", (var_from_col, 1, var_to_col))  # ToCol = FromCol + 1
    ]
    
    logic_engine.add_rule(head, body)
    
    # 2 up, 1 left
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_from_row, 2, var_to_row)),  # ToRow = FromRow - 2
        ("subtract", (var_from_col, 1, var_to_col))  # ToCol = FromCol - 1
    ]
    
    logic_engine.add_rule(head, body)
    
    # 2 down, 1 right
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("add", (var_from_row, 2, var_to_row)),  # ToRow = FromRow + 2
        ("add", (var_from_col, 1, var_to_col))  # ToCol = FromCol + 1
    ]
    
    logic_engine.add_rule(head, body)
    
    # 2 down, 1 left
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("add", (var_from_row, 2, var_to_row)),  # ToRow = FromRow + 2
        ("subtract", (var_from_col, 1, var_to_col))  # ToCol = FromCol - 1
    ]
    
    logic_engine.add_rule(head, body)
    
    # 2 right, 1 up
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_from_row, 1, var_to_row)),  # ToRow = FromRow - 1
        ("add", (var_from_col, 2, var_to_col))  # ToCol = FromCol + 2
    ]
    
    logic_engine.add_rule(head, body)
    
    # 2 right, 1 down
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("add", (var_from_row, 1, var_to_row)),  # ToRow = FromRow + 1
        ("add", (var_from_col, 2, var_to_col))  # ToCol = FromCol + 2
    ]
    
    logic_engine.add_rule(head, body)
    
    # 2 left, 1 up
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_from_row, 1, var_to_row)),  # ToRow = FromRow - 1
        ("subtract", (var_from_col, 2, var_to_col))  # ToCol = FromCol - 2
    ]
    
    logic_engine.add_rule(head, body)
    
    # 2 left, 1 down
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("add", (var_from_row, 1, var_to_row)),  # ToRow = FromRow + 1
        ("subtract", (var_from_col, 2, var_to_col))  # ToCol = FromCol - 2
    ]
    
    logic_engine.add_rule(head, body)


def setup_knight_captures(logic_engine):
    """
    Setup capture rules for knights.
    Knight captures are the same as movement patterns.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_player = logic_engine.variable("Player")
    
    # For knights, the PIECE_CAPTURE predicate patterns are the same as PIECE_MOVE
    # This is because knights can jump over pieces and capture in any of their L-shaped patterns
    
    # 2 up, 1 right
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_from_row, 2, var_to_row)),  # ToRow = FromRow - 2
        ("add", (var_from_col, 1, var_to_col))  # ToCol = FromCol + 1
    ]
    
    logic_engine.add_rule(head, body)
    
    # 2 up, 1 left
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_from_row, 2, var_to_row)),  # ToRow = FromRow - 2
        ("subtract", (var_from_col, 1, var_to_col))  # ToCol = FromCol - 1
    ]
    
    logic_engine.add_rule(head, body)
    
    # 2 down, 1 right
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("add", (var_from_row, 2, var_to_row)),  # ToRow = FromRow + 2
        ("add", (var_from_col, 1, var_to_col))  # ToCol = FromCol + 1
    ]
    
    logic_engine.add_rule(head, body)
    
    # 2 down, 1 left
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("add", (var_from_row, 2, var_to_row)),  # ToRow = FromRow + 2
        ("subtract", (var_from_col, 1, var_to_col))  # ToCol = FromCol - 1
    ]
    
    logic_engine.add_rule(head, body)
    
    # 2 right, 1 up
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_from_row, 1, var_to_row)),  # ToRow = FromRow - 1
        ("add", (var_from_col, 2, var_to_col))  # ToCol = FromCol + 2
    ]
    
    logic_engine.add_rule(head, body)
    
    # 2 right, 1 down
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("add", (var_from_row, 1, var_to_row)),  # ToRow = FromRow + 1
        ("add", (var_from_col, 2, var_to_col))  # ToCol = FromCol + 2
    ]
    
    logic_engine.add_rule(head, body)
    
    # 2 left, 1 up
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_from_row, 1, var_to_row)),  # ToRow = FromRow - 1
        ("subtract", (var_from_col, 2, var_to_col))  # ToCol = FromCol - 2
    ]
    
    logic_engine.add_rule(head, body)
    
    # 2 left, 1 down
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.KNIGHT, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("add", (var_from_row, 1, var_to_row)),  # ToRow = FromRow + 1
        ("subtract", (var_from_col, 2, var_to_col))  # ToCol = FromCol - 2
    ]
    
    logic_engine.add_rule(head, body)
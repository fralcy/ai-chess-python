"""
Rules for determining if a move is blocked by another piece.
"""

from src.logic_engine.predicates import ChessPredicates


def setup_blocking_rules(logic_engine):
    """
    Setup rules for determining if a move path is blocked.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Horizontal, vertical, and diagonal blocking rules
    setup_horizontal_blocking(logic_engine)
    setup_vertical_blocking(logic_engine)
    setup_diagonal_blocking(logic_engine)


def setup_horizontal_blocking(logic_engine):
    """
    Setup rules for horizontal blocking.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # is_blocked_horizontal(FromRow, FromCol, ToRow, ToCol) :-
    #     FromRow = ToRow,  # Horizontal movement
    #     FromCol < ToCol,  # Moving right
    #     BlockCol is FromCol + 1,
    #     BlockCol < ToCol,
    #     piece_at(_, _, FromRow, BlockCol).
    
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_block_col = logic_engine.variable("BlockCol")
    var_any_type = logic_engine.variable("AnyType")
    var_any_player = logic_engine.variable("AnyPlayer")
    
    # Moving right
    head = (ChessPredicates.IS_BLOCKED, 
            (var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("equal", (var_from_row, var_to_row)),  # Horizontal movement
        ("less_than", (var_from_col, var_to_col)),  # Moving right
        ("add", (var_from_col, 1, var_block_col)),  # BlockCol = FromCol + 1
        ("less_than", (var_block_col, var_to_col)),  # BlockCol < ToCol
        (ChessPredicates.PIECE_AT, 
         (var_any_type, var_any_player, var_from_row, var_block_col))  # Piece at blocking position
    ]
    
    logic_engine.add_rule(head, body)
    
    # Moving left
    head = (ChessPredicates.IS_BLOCKED, 
            (var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("equal", (var_from_row, var_to_row)),  # Horizontal movement
        ("greater_than", (var_from_col, var_to_col)),  # Moving left
        ("subtract", (var_from_col, 1, var_block_col)),  # BlockCol = FromCol - 1
        ("greater_than", (var_block_col, var_to_col)),  # BlockCol > ToCol
        (ChessPredicates.PIECE_AT, 
         (var_any_type, var_any_player, var_from_row, var_block_col))  # Piece at blocking position
    ]
    
    logic_engine.add_rule(head, body)


def setup_vertical_blocking(logic_engine):
    """
    Setup rules for vertical blocking.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # is_blocked_vertical(FromRow, FromCol, ToRow, ToCol) :-
    #     FromCol = ToCol,  # Vertical movement
    #     FromRow < ToRow,  # Moving down
    #     BlockRow is FromRow + 1,
    #     BlockRow < ToRow,
    #     piece_at(_, _, BlockRow, FromCol).
    
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_block_row = logic_engine.variable("BlockRow")
    var_any_type = logic_engine.variable("AnyType")
    var_any_player = logic_engine.variable("AnyPlayer")
    
    # Moving down
    head = (ChessPredicates.IS_BLOCKED, 
            (var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("equal", (var_from_col, var_to_col)),  # Vertical movement
        ("less_than", (var_from_row, var_to_row)),  # Moving down
        ("add", (var_from_row, 1, var_block_row)),  # BlockRow = FromRow + 1
        ("less_than", (var_block_row, var_to_row)),  # BlockRow < ToRow
        (ChessPredicates.PIECE_AT, 
         (var_any_type, var_any_player, var_block_row, var_from_col))  # Piece at blocking position
    ]
    
    logic_engine.add_rule(head, body)
    
    # Moving up
    head = (ChessPredicates.IS_BLOCKED, 
            (var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("equal", (var_from_col, var_to_col)),  # Vertical movement
        ("greater_than", (var_from_row, var_to_row)),  # Moving up
        ("subtract", (var_from_row, 1, var_block_row)),  # BlockRow = FromRow - 1
        ("greater_than", (var_block_row, var_to_row)),  # BlockRow > ToRow
        (ChessPredicates.PIECE_AT, 
         (var_any_type, var_any_player, var_block_row, var_from_col))  # Piece at blocking position
    ]
    
    logic_engine.add_rule(head, body)


def setup_diagonal_blocking(logic_engine):
    """
    Setup rules for diagonal blocking.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Northeast diagonal
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_block_row = logic_engine.variable("BlockRow")
    var_block_col = logic_engine.variable("BlockCol")
    var_any_type = logic_engine.variable("AnyType")
    var_any_player = logic_engine.variable("AnyPlayer")
    var_row_diff = logic_engine.variable("RowDiff")
    var_col_diff = logic_engine.variable("ColDiff")
    
    # Northeast
    head = (ChessPredicates.IS_BLOCKED, 
            (var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_from_row, var_to_row, var_row_diff)),  # RowDiff = FromRow - ToRow
        ("subtract", (var_to_col, var_from_col, var_col_diff)),  # ColDiff = ToCol - FromCol
        ("equal", (var_row_diff, var_col_diff)),  # RowDiff = ColDiff (diagonal)
        ("greater_than", (var_row_diff, 0)),  # Moving up
        ("greater_than", (var_col_diff, 0)),  # Moving right
        ("subtract", (var_from_row, 1, var_block_row)),  # BlockRow = FromRow - 1
        ("add", (var_from_col, 1, var_block_col)),  # BlockCol = FromCol + 1
        ("greater_than", (var_block_row, var_to_row)),  # BlockRow > ToRow
        ("less_than", (var_block_col, var_to_col)),  # BlockCol < ToCol
        (ChessPredicates.PIECE_AT, 
         (var_any_type, var_any_player, var_block_row, var_block_col))  # Piece at blocking position
    ]
    
    logic_engine.add_rule(head, body)
    
    # Southeast
    head = (ChessPredicates.IS_BLOCKED, 
            (var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_to_row, var_from_row, var_row_diff)),  # RowDiff = ToRow - FromRow
        ("subtract", (var_to_col, var_from_col, var_col_diff)),  # ColDiff = ToCol - FromCol
        ("equal", (var_row_diff, var_col_diff)),  # RowDiff = ColDiff (diagonal)
        ("greater_than", (var_row_diff, 0)),  # Moving down
        ("greater_than", (var_col_diff, 0)),  # Moving right
        ("add", (var_from_row, 1, var_block_row)),  # BlockRow = FromRow + 1
        ("add", (var_from_col, 1, var_block_col)),  # BlockCol = FromCol + 1
        ("less_than", (var_block_row, var_to_row)),  # BlockRow < ToRow
        ("less_than", (var_block_col, var_to_col)),  # BlockCol < ToCol
        (ChessPredicates.PIECE_AT, 
         (var_any_type, var_any_player, var_block_row, var_block_col))  # Piece at blocking position
    ]
    
    logic_engine.add_rule(head, body)
    
    # Southwest
    head = (ChessPredicates.IS_BLOCKED, 
            (var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_to_row, var_from_row, var_row_diff)),  # RowDiff = ToRow - FromRow
        ("subtract", (var_from_col, var_to_col, var_col_diff)),  # ColDiff = FromCol - ToCol
        ("equal", (var_row_diff, var_col_diff)),  # RowDiff = ColDiff (diagonal)
        ("greater_than", (var_row_diff, 0)),  # Moving down
        ("greater_than", (var_col_diff, 0)),  # Moving left
        ("add", (var_from_row, 1, var_block_row)),  # BlockRow = FromRow + 1
        ("subtract", (var_from_col, 1, var_block_col)),  # BlockCol = FromCol - 1
        ("less_than", (var_block_row, var_to_row)),  # BlockRow < ToRow
        ("greater_than", (var_block_col, var_to_col)),  # BlockCol > ToCol
        (ChessPredicates.PIECE_AT, 
         (var_any_type, var_any_player, var_block_row, var_block_col))  # Piece at blocking position
    ]
    
    logic_engine.add_rule(head, body)
    
    # Northwest
    head = (ChessPredicates.IS_BLOCKED, 
            (var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_from_row, var_to_row, var_row_diff)),  # RowDiff = FromRow - ToRow
        ("subtract", (var_from_col, var_to_col, var_col_diff)),  # ColDiff = FromCol - ToCol
        ("equal", (var_row_diff, var_col_diff)),  # RowDiff = ColDiff (diagonal)
        ("greater_than", (var_row_diff, 0)),  # Moving up
        ("greater_than", (var_col_diff, 0)),  # Moving left
        ("subtract", (var_from_row, 1, var_block_row)),  # BlockRow = FromRow - 1
        ("subtract", (var_from_col, 1, var_block_col)),  # BlockCol = FromCol - 1
        ("greater_than", (var_block_row, var_to_row)),  # BlockRow > ToRow
        ("greater_than", (var_block_col, var_to_col)),  # BlockCol > ToCol
        (ChessPredicates.PIECE_AT, 
         (var_any_type, var_any_player, var_block_row, var_block_col))  # Piece at blocking position
    ]
    
    logic_engine.add_rule(head, body)
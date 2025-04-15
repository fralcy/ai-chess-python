"""
Movement rules for pawns.
"""

from src.logic_engine.piece_type import PieceType
from src.logic_engine.player import Player
from src.logic_engine.predicates import ChessPredicates


def setup_pawn_rules(logic_engine):
    """
    Setup movement rules for pawns.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Setup basic pawn movement rules
    setup_pawn_forward_move(logic_engine)
    setup_pawn_double_move(logic_engine)
    setup_pawn_capture(logic_engine)


def setup_pawn_forward_move(logic_engine):
    """
    Setup rules for a pawn moving forward.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # piece_move(PAWN, WHITE, FromRow, FromCol, ToRow, ToCol) :-
    #     ToRow is FromRow - 1,     # White pawns move up (decreasing row)
    #     ToCol = FromCol,          # Same column
    #     not(piece_at(_, _, ToRow, ToCol)).  # Target square is empty
    
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_any_type = logic_engine.variable("AnyType")
    var_any_player = logic_engine.variable("AnyPlayer")
    
    # White pawn moves up
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.PAWN, Player.WHITE, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_from_row, 1, var_to_row)),  # ToRow = FromRow - 1
        ("equal", (var_from_col, var_to_col)),  # ToCol = FromCol
        ("not", ((ChessPredicates.PIECE_AT, 
                  (var_any_type, var_any_player, var_to_row, var_to_col))))  # No piece at target
    ]
    
    logic_engine.add_rule(head, body)
    
    # piece_move(PAWN, BLACK, FromRow, FromCol, ToRow, ToCol) :-
    #     ToRow is FromRow + 1,     # Black pawns move down (increasing row)
    #     ToCol = FromCol,          # Same column
    #     not(piece_at(_, _, ToRow, ToCol)).  # Target square is empty
    
    # Black pawn moves down
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.PAWN, Player.BLACK, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("add", (var_from_row, 1, var_to_row)),  # ToRow = FromRow + 1
        ("equal", (var_from_col, var_to_col)),  # ToCol = FromCol
        ("not", ((ChessPredicates.PIECE_AT, 
                  (var_any_type, var_any_player, var_to_row, var_to_col))))  # No piece at target
    ]
    
    logic_engine.add_rule(head, body)


def setup_pawn_double_move(logic_engine):
    """
    Setup rules for a pawn's double move from the starting position.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # piece_move(PAWN, WHITE, FromRow, FromCol, ToRow, ToCol) :-
    #     FromRow = 6,              # White pawn's starting row
    #     ToRow is FromRow - 2,     # Move 2 squares up
    #     ToCol = FromCol,          # Same column
    #     not(piece_at(_, _, FromRow - 1, FromCol)),  # No piece blocking
    #     not(piece_at(_, _, ToRow, ToCol)).  # Target square is empty
    
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_intermediate_row = logic_engine.variable("IntermediateRow")
    var_any_type = logic_engine.variable("AnyType")
    var_any_player = logic_engine.variable("AnyPlayer")
    
    # White pawn double move
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.PAWN, Player.WHITE, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("equal", (var_from_row, 6)),  # FromRow = 6 (starting row for white pawns)
        ("subtract", (var_from_row, 2, var_to_row)),  # ToRow = FromRow - 2
        ("equal", (var_from_col, var_to_col)),  # ToCol = FromCol
        ("subtract", (var_from_row, 1, var_intermediate_row)),  # IntermediateRow = FromRow - 1
        ("not", ((ChessPredicates.PIECE_AT, 
                  (var_any_type, var_any_player, var_intermediate_row, var_from_col)))),  # No piece blocking
        ("not", ((ChessPredicates.PIECE_AT, 
                  (var_any_type, var_any_player, var_to_row, var_to_col))))  # No piece at target
    ]
    
    logic_engine.add_rule(head, body)
    
    # piece_move(PAWN, BLACK, FromRow, FromCol, ToRow, ToCol) :-
    #     FromRow = 1,              # Black pawn's starting row
    #     ToRow is FromRow + 2,     # Move 2 squares down
    #     ToCol = FromCol,          # Same column
    #     not(piece_at(_, _, FromRow + 1, FromCol)),  # No piece blocking
    #     not(piece_at(_, _, ToRow, ToCol)).  # Target square is empty
    
    # Black pawn double move
    head = (ChessPredicates.PIECE_MOVE, 
            (PieceType.PAWN, Player.BLACK, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("equal", (var_from_row, 1)),  # FromRow = 1 (starting row for black pawns)
        ("add", (var_from_row, 2, var_to_row)),  # ToRow = FromRow + 2
        ("equal", (var_from_col, var_to_col)),  # ToCol = FromCol
        ("add", (var_from_row, 1, var_intermediate_row)),  # IntermediateRow = FromRow + 1
        ("not", ((ChessPredicates.PIECE_AT, 
                  (var_any_type, var_any_player, var_intermediate_row, var_from_col)))),  # No piece blocking
        ("not", ((ChessPredicates.PIECE_AT, 
                  (var_any_type, var_any_player, var_to_row, var_to_col))))  # No piece at target
    ]
    
    logic_engine.add_rule(head, body)


def setup_pawn_capture(logic_engine):
    """
    Setup rules for a pawn capturing diagonally.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # piece_capture(PAWN, WHITE, FromRow, FromCol, ToRow, ToCol) :-
    #     ToRow is FromRow - 1,     # Move up one row
    #     (ToCol is FromCol - 1; ToCol is FromCol + 1),  # Move left or right
    #     piece_at(_, BLACK, ToRow, ToCol).  # Black piece at target
    
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_any_type = logic_engine.variable("AnyType")
    
    # White pawn captures to the left
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.PAWN, Player.WHITE, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_from_row, 1, var_to_row)),  # ToRow = FromRow - 1
        ("subtract", (var_from_col, 1, var_to_col)),  # ToCol = FromCol - 1
        (ChessPredicates.PIECE_AT, 
         (var_any_type, Player.BLACK, var_to_row, var_to_col))  # Black piece at target
    ]
    
    logic_engine.add_rule(head, body)
    
    # White pawn captures to the right
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.PAWN, Player.WHITE, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("subtract", (var_from_row, 1, var_to_row)),  # ToRow = FromRow - 1
        ("add", (var_from_col, 1, var_to_col)),  # ToCol = FromCol + 1
        (ChessPredicates.PIECE_AT, 
         (var_any_type, Player.BLACK, var_to_row, var_to_col))  # Black piece at target
    ]
    
    logic_engine.add_rule(head, body)
    
    # piece_capture(PAWN, BLACK, FromRow, FromCol, ToRow, ToCol) :-
    #     ToRow is FromRow + 1,     # Move down one row
    #     (ToCol is FromCol - 1; ToCol is FromCol + 1),  # Move left or right
    #     piece_at(_, WHITE, ToRow, ToCol).  # White piece at target
    
    # Black pawn captures to the left
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.PAWN, Player.BLACK, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("add", (var_from_row, 1, var_to_row)),  # ToRow = FromRow + 1
        ("subtract", (var_from_col, 1, var_to_col)),  # ToCol = FromCol - 1
        (ChessPredicates.PIECE_AT, 
         (var_any_type, Player.WHITE, var_to_row, var_to_col))  # White piece at target
    ]
    
    logic_engine.add_rule(head, body)
    
    # Black pawn captures to the right
    head = (ChessPredicates.PIECE_CAPTURE, 
            (PieceType.PAWN, Player.BLACK, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        ("add", (var_from_row, 1, var_to_row)),  # ToRow = FromRow + 1
        ("add", (var_from_col, 1, var_to_col)),  # ToCol = FromCol + 1
        (ChessPredicates.PIECE_AT, 
         (var_any_type, Player.WHITE, var_to_row, var_to_col))  # White piece at target
    ]
    
    logic_engine.add_rule(head, body)
"""
En passant rules for pawns.
Defines the logic for en passant captures.
"""

from src.logic_engine.piece_type import PieceType
from src.logic_engine.player import Player
from src.logic_engine.predicates import ChessPredicates


def setup_en_passant_rules(logic_engine):
    """
    Setup en passant rules for pawns.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # En passant is when a pawn captures an opponent's pawn that has just made a two-square advance
    # The capturing pawn must be on the fifth rank (from its perspective)
    # The captured pawn must have just moved two squares forward from its starting position
    # The captured pawn is removed from the board
    
    setup_white_en_passant(logic_engine)
    setup_black_en_passant(logic_engine)


def setup_white_en_passant(logic_engine):
    """
    Setup en passant rules for white pawns.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # can_en_passant(WHITE, FromRow, FromCol, ToRow, ToCol) :-
    #     FromRow == 3,  # White pawn on the fifth rank
    #     piece_at(PAWN, WHITE, FromRow, FromCol),
    #     (ToCol == FromCol + 1; ToCol == FromCol - 1),  # Move diagonally
    #     ToRow == FromRow - 1,  # Move forward
    #     pawn_skip(BLACK, ToRow + 1, ToCol).  # Black pawn just moved two squares
    
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_capture_row = logic_engine.variable("CaptureRow")
    var_capture_col = logic_engine.variable("CaptureCol")
    
    # White en passant to the right
    head = (ChessPredicates.CAN_EN_PASSANT, 
            (Player.WHITE, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        # White pawn on the fifth rank
        ("equal", (var_from_row, 3)),
        (ChessPredicates.PIECE_AT, 
         (PieceType.PAWN, Player.WHITE, var_from_row, var_from_col)),
        
        # Diagonal capture to the right
        ("add", (var_from_col, 1, var_to_col)),
        
        # Move one row forward
        ("subtract", (var_from_row, 1, var_to_row)),
        
        # Black pawn just moved two squares
        ("add", (var_to_row, 1, var_capture_row)),
        ("equal", (var_capture_col, var_to_col)),  # Same column as target
        (ChessPredicates.PIECE_AT, 
         (PieceType.PAWN, Player.BLACK, var_capture_row, var_capture_col)),
        (ChessPredicates.PAWN_SKIP, 
         (Player.BLACK, var_capture_row, var_capture_col))
    ]
    
    logic_engine.add_rule(head, body)
    
    # White en passant to the left
    head = (ChessPredicates.CAN_EN_PASSANT, 
            (Player.WHITE, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        # White pawn on the fifth rank
        ("equal", (var_from_row, 3)),
        (ChessPredicates.PIECE_AT, 
         (PieceType.PAWN, Player.WHITE, var_from_row, var_from_col)),
        
        # Diagonal capture to the left
        ("subtract", (var_from_col, 1, var_to_col)),
        
        # Move one row forward
        ("subtract", (var_from_row, 1, var_to_row)),
        
        # Black pawn just moved two squares
        ("add", (var_to_row, 1, var_capture_row)),
        ("equal", (var_capture_col, var_to_col)),  # Same column as target
        (ChessPredicates.PIECE_AT, 
         (PieceType.PAWN, Player.BLACK, var_capture_row, var_capture_col)),
        (ChessPredicates.PAWN_SKIP, 
         (Player.BLACK, var_capture_row, var_capture_col))
    ]
    
    logic_engine.add_rule(head, body)


def setup_black_en_passant(logic_engine):
    """
    Setup en passant rules for black pawns.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # can_en_passant(BLACK, FromRow, FromCol, ToRow, ToCol) :-
    #     FromRow == 4,  # Black pawn on the fifth rank
    #     piece_at(PAWN, BLACK, FromRow, FromCol),
    #     (ToCol == FromCol + 1; ToCol == FromCol - 1),  # Move diagonally
    #     ToRow == FromRow + 1,  # Move forward
    #     pawn_skip(WHITE, ToRow - 1, ToCol).  # White pawn just moved two squares
    
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_capture_row = logic_engine.variable("CaptureRow")
    var_capture_col = logic_engine.variable("CaptureCol")
    
    # Black en passant to the right
    head = (ChessPredicates.CAN_EN_PASSANT, 
            (Player.BLACK, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        # Black pawn on the fifth rank
        ("equal", (var_from_row, 4)),
        (ChessPredicates.PIECE_AT, 
         (PieceType.PAWN, Player.BLACK, var_from_row, var_from_col)),
        
        # Diagonal capture to the right
        ("add", (var_from_col, 1, var_to_col)),
        
        # Move one row forward
        ("add", (var_from_row, 1, var_to_row)),
        
        # White pawn just moved two squares
        ("subtract", (var_to_row, 1, var_capture_row)),
        ("equal", (var_capture_col, var_to_col)),  # Same column as target
        (ChessPredicates.PIECE_AT, 
         (PieceType.PAWN, Player.WHITE, var_capture_row, var_capture_col)),
        (ChessPredicates.PAWN_SKIP, 
         (Player.WHITE, var_capture_row, var_capture_col))
    ]
    
    logic_engine.add_rule(head, body)
    
    # Black en passant to the left
    head = (ChessPredicates.CAN_EN_PASSANT, 
            (Player.BLACK, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        # Black pawn on the fifth rank
        ("equal", (var_from_row, 4)),
        (ChessPredicates.PIECE_AT, 
         (PieceType.PAWN, Player.BLACK, var_from_row, var_from_col)),
        
        # Diagonal capture to the left
        ("subtract", (var_from_col, 1, var_to_col)),
        
        # Move one row forward
        ("add", (var_from_row, 1, var_to_row)),
        
        # White pawn just moved two squares
        ("subtract", (var_to_row, 1, var_capture_row)),
        ("equal", (var_capture_col, var_to_col)),  # Same column as target
        (ChessPredicates.PIECE_AT, 
         (PieceType.PAWN, Player.WHITE, var_capture_row, var_capture_col)),
        (ChessPredicates.PAWN_SKIP, 
         (Player.WHITE, var_capture_row, var_capture_col))
    ]
    
    logic_engine.add_rule(head, body)
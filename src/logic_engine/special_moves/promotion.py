"""
Promotion rules for pawns.
Defines the logic for pawn promotion when reaching the opposite edge of the board.
"""

from src.logic_engine.piece_type import PieceType
from src.logic_engine.player import Player
from src.logic_engine.predicates import ChessPredicates


def setup_promotion_rules(logic_engine):
    """
    Setup promotion rules for pawns.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Setup promotion rules for forward moves and captures
    setup_white_promotion(logic_engine)
    setup_black_promotion(logic_engine)


def setup_white_promotion(logic_engine):
    """
    Setup promotion rules for white pawns.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # can_promote(WHITE, FromRow, FromCol, ToRow, ToCol, NewType) :-
    #     FromRow == 1,  # White pawn on the second-to-last rank
    #     ToRow == 0,    # Moving to the last rank
    #     piece_at(PAWN, WHITE, FromRow, FromCol),
    #     (
    #         (ToCol == FromCol, not(piece_at(_, _, ToRow, ToCol))) |  # Moving forward
    #         ((ToCol == FromCol + 1 | ToCol == FromCol - 1), piece_at(_, BLACK, ToRow, ToCol))  # Capturing
    #     ),
    #     NewType in [QUEEN, ROOK, BISHOP, KNIGHT].
    
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_any_type = logic_engine.variable("AnyType")
    var_any_player = logic_engine.variable("AnyPlayer")
    
    # White pawn promotion - forward move
    for piece_type in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
        head = (ChessPredicates.CAN_PROMOTE, 
                (Player.WHITE, var_from_row, var_from_col, var_to_row, var_to_col, piece_type))
        
        body = [
            # White pawn on the second-to-last rank
            ("equal", (var_from_row, 1)),
            (ChessPredicates.PIECE_AT, 
             (PieceType.PAWN, Player.WHITE, var_from_row, var_from_col)),
            
            # Moving to the last rank
            ("equal", (var_to_row, 0)),
            
            # Move forward
            ("equal", (var_from_col, var_to_col)),
            
            # Target square must be empty
            ("not", ((ChessPredicates.PIECE_AT, 
                    (var_any_type, var_any_player, var_to_row, var_to_col))))
        ]
        
        logic_engine.add_rule(head, body)
    
    # White pawn promotion - capture to the right
    for piece_type in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
        head = (ChessPredicates.CAN_PROMOTE, 
                (Player.WHITE, var_from_row, var_from_col, var_to_row, var_to_col, piece_type))
        
        body = [
            # White pawn on the second-to-last rank
            ("equal", (var_from_row, 1)),
            (ChessPredicates.PIECE_AT, 
             (PieceType.PAWN, Player.WHITE, var_from_row, var_from_col)),
            
            # Moving to the last rank
            ("equal", (var_to_row, 0)),
            
            # Capture to the right
            ("add", (var_from_col, 1, var_to_col)),
            
            # Target square must contain a black piece
            (ChessPredicates.PIECE_AT, 
             (var_any_type, Player.BLACK, var_to_row, var_to_col))
        ]
        
        logic_engine.add_rule(head, body)
    
    # White pawn promotion - capture to the left
    for piece_type in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
        head = (ChessPredicates.CAN_PROMOTE, 
                (Player.WHITE, var_from_row, var_from_col, var_to_row, var_to_col, piece_type))
        
        body = [
            # White pawn on the second-to-last rank
            ("equal", (var_from_row, 1)),
            (ChessPredicates.PIECE_AT, 
             (PieceType.PAWN, Player.WHITE, var_from_row, var_from_col)),
            
            # Moving to the last rank
            ("equal", (var_to_row, 0)),
            
            # Capture to the left
            ("subtract", (var_from_col, 1, var_to_col)),
            
            # Target square must contain a black piece
            (ChessPredicates.PIECE_AT, 
             (var_any_type, Player.BLACK, var_to_row, var_to_col))
        ]
        
        logic_engine.add_rule(head, body)


def setup_black_promotion(logic_engine):
    """
    Setup promotion rules for black pawns.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # can_promote(BLACK, FromRow, FromCol, ToRow, ToCol, NewType) :-
    #     FromRow == 6,  # Black pawn on the second-to-last rank
    #     ToRow == 7,    # Moving to the last rank
    #     piece_at(PAWN, BLACK, FromRow, FromCol),
    #     (
    #         (ToCol == FromCol, not(piece_at(_, _, ToRow, ToCol))) |  # Moving forward
    #         ((ToCol == FromCol + 1 | ToCol == FromCol - 1), piece_at(_, WHITE, ToRow, ToCol))  # Capturing
    #     ),
    #     NewType in [QUEEN, ROOK, BISHOP, KNIGHT].
    
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_any_type = logic_engine.variable("AnyType")
    var_any_player = logic_engine.variable("AnyPlayer")
    
    # Black pawn promotion - forward move
    for piece_type in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
        head = (ChessPredicates.CAN_PROMOTE, 
                (Player.BLACK, var_from_row, var_from_col, var_to_row, var_to_col, piece_type))
        
        body = [
            # Black pawn on the second-to-last rank
            ("equal", (var_from_row, 6)),
            (ChessPredicates.PIECE_AT, 
             (PieceType.PAWN, Player.BLACK, var_from_row, var_from_col)),
            
            # Moving to the last rank
            ("equal", (var_to_row, 7)),
            
            # Move forward
            ("equal", (var_from_col, var_to_col)),
            
            # Target square must be empty
            ("not", ((ChessPredicates.PIECE_AT, 
                    (var_any_type, var_any_player, var_to_row, var_to_col))))
        ]
        
        logic_engine.add_rule(head, body)
    
    # Black pawn promotion - capture to the right
    for piece_type in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
        head = (ChessPredicates.CAN_PROMOTE, 
                (Player.BLACK, var_from_row, var_from_col, var_to_row, var_to_col, piece_type))
        
        body = [
            # Black pawn on the second-to-last rank
            ("equal", (var_from_row, 6)),
            (ChessPredicates.PIECE_AT, 
             (PieceType.PAWN, Player.BLACK, var_from_row, var_from_col)),
            
            # Moving to the last rank
            ("equal", (var_to_row, 7)),
            
            # Capture to the right
            ("add", (var_from_col, 1, var_to_col)),
            
            # Target square must contain a white piece
            (ChessPredicates.PIECE_AT, 
             (var_any_type, Player.WHITE, var_to_row, var_to_col))
        ]
        
        logic_engine.add_rule(head, body)
    
    # Black pawn promotion - capture to the left
    for piece_type in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
        head = (ChessPredicates.CAN_PROMOTE, 
                (Player.BLACK, var_from_row, var_from_col, var_to_row, var_to_col, piece_type))
        
        body = [
            # Black pawn on the second-to-last rank
            ("equal", (var_from_row, 6)),
            (ChessPredicates.PIECE_AT, 
             (PieceType.PAWN, Player.BLACK, var_from_row, var_from_col)),
            
            # Moving to the last rank
            ("equal", (var_to_row, 7)),
            
            # Capture to the left
            ("subtract", (var_from_col, 1, var_to_col)),
            
            # Target square must contain a white piece
            (ChessPredicates.PIECE_AT, 
             (var_any_type, Player.WHITE, var_to_row, var_to_col))
        ]
        
        logic_engine.add_rule(head, body)
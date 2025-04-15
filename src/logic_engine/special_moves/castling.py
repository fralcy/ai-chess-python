"""
Castling rules for kings.
Defines the logic for kingside and queenside castling.
"""

from src.logic_engine.piece_type import PieceType
from src.logic_engine.player import Player
from src.logic_engine.predicates import ChessPredicates


def setup_castling_rules(logic_engine):
    """
    Setup castling rules for kings.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Setup kingside castling rules
    setup_kingside_castling(logic_engine)
    
    # Setup queenside castling rules
    setup_queenside_castling(logic_engine)


def setup_kingside_castling(logic_engine):
    """
    Setup kingside castling rules.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # can_castle(Player, 'kingside', FromRow, FromCol, ToRow, ToCol) :-
    #     Player == WHITE,
    #     FromRow == 7, FromCol == 4,  # White king's initial position
    #     ToRow == 7, ToCol == 6,      # Castled king position
    #     not(has_moved(KING, Player, FromRow, FromCol, true)),  # King hasn't moved
    #     piece_at(ROOK, Player, 7, 7),    # Rook is in the right corner
    #     not(has_moved(ROOK, Player, 7, 7, true)),  # Rook hasn't moved
    #     not(piece_at(_, _, 7, 5)),   # No piece between king and rook
    #     not(piece_at(_, _, 7, 6)),
    #     not(is_king_in_check(Player)),  # King is not in check
    #     not(would_be_in_check(Player, 7, 5)),  # King doesn't pass through check
    #     not(would_be_in_check(Player, 7, 6)).  # King doesn't end in check
    
    var_any_type = logic_engine.variable("AnyType")
    var_any_player = logic_engine.variable("AnyPlayer")
    
    # White kingside castling
    head = (ChessPredicates.CAN_CASTLE, 
            (Player.WHITE, "kingside", 7, 4, 7, 6))
    
    body = [
        # King must not have moved
        (ChessPredicates.HAS_MOVED, 
         (PieceType.KING, Player.WHITE, 7, 4, False)),
        
        # Rook must be present and not have moved
        (ChessPredicates.PIECE_AT, 
         (PieceType.ROOK, Player.WHITE, 7, 7)),
        (ChessPredicates.HAS_MOVED, 
         (PieceType.ROOK, Player.WHITE, 7, 7, False)),
        
        # Squares between king and rook must be empty
        ("not", ((ChessPredicates.PIECE_AT, 
                (var_any_type, var_any_player, 7, 5)))),
        ("not", ((ChessPredicates.PIECE_AT, 
                (var_any_type, var_any_player, 7, 6)))),
        
        # King must not be in check or pass through check
        ("not", ((ChessPredicates.IN_CHECK, 
                (Player.WHITE)))),
        ("not", ((ChessPredicates.SQUARE_ATTACKED, 
                (Player.BLACK, 7, 5)))),
        ("not", ((ChessPredicates.SQUARE_ATTACKED, 
                (Player.BLACK, 7, 6))))
    ]
    
    logic_engine.add_rule(head, body)
    
    # Black kingside castling
    head = (ChessPredicates.CAN_CASTLE, 
            (Player.BLACK, "kingside", 0, 4, 0, 6))
    
    body = [
        # King must not have moved
        (ChessPredicates.HAS_MOVED, 
         (PieceType.KING, Player.BLACK, 0, 4, False)),
        
        # Rook must be present and not have moved
        (ChessPredicates.PIECE_AT, 
         (PieceType.ROOK, Player.BLACK, 0, 7)),
        (ChessPredicates.HAS_MOVED, 
         (PieceType.ROOK, Player.BLACK, 0, 7, False)),
        
        # Squares between king and rook must be empty
        ("not", ((ChessPredicates.PIECE_AT, 
                (var_any_type, var_any_player, 0, 5)))),
        ("not", ((ChessPredicates.PIECE_AT, 
                (var_any_type, var_any_player, 0, 6)))),
        
        # King must not be in check or pass through check
        ("not", ((ChessPredicates.IN_CHECK, 
                (Player.BLACK)))),
        ("not", ((ChessPredicates.SQUARE_ATTACKED, 
                (Player.WHITE, 0, 5)))),
        ("not", ((ChessPredicates.SQUARE_ATTACKED, 
                (Player.WHITE, 0, 6))))
    ]
    
    logic_engine.add_rule(head, body)


def setup_queenside_castling(logic_engine):
    """
    Setup queenside castling rules.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # can_castle(Player, 'queenside', FromRow, FromCol, ToRow, ToCol) :-
    #     Player == WHITE,
    #     FromRow == 7, FromCol == 4,  # White king's initial position
    #     ToRow == 7, ToCol == 2,      # Castled king position
    #     not(has_moved(KING, Player, FromRow, FromCol, true)),  # King hasn't moved
    #     piece_at(ROOK, Player, 7, 0),    # Rook is in the left corner
    #     not(has_moved(ROOK, Player, 7, 0, true)),  # Rook hasn't moved
    #     not(piece_at(_, _, 7, 1)),   # No piece between king and rook
    #     not(piece_at(_, _, 7, 2)),
    #     not(piece_at(_, _, 7, 3)),
    #     not(is_king_in_check(Player)),  # King is not in check
    #     not(would_be_in_check(Player, 7, 3)),  # King doesn't pass through check
    #     not(would_be_in_check(Player, 7, 2)).  # King doesn't end in check
    
    var_any_type = logic_engine.variable("AnyType")
    var_any_player = logic_engine.variable("AnyPlayer")
    
    # White queenside castling
    head = (ChessPredicates.CAN_CASTLE, 
            (Player.WHITE, "queenside", 7, 4, 7, 2))
    
    body = [
        # King must not have moved
        (ChessPredicates.HAS_MOVED, 
         (PieceType.KING, Player.WHITE, 7, 4, False)),
        
        # Rook must be present and not have moved
        (ChessPredicates.PIECE_AT, 
         (PieceType.ROOK, Player.WHITE, 7, 0)),
        (ChessPredicates.HAS_MOVED, 
         (PieceType.ROOK, Player.WHITE, 7, 0, False)),
        
        # Squares between king and rook must be empty
        ("not", ((ChessPredicates.PIECE_AT, 
                (var_any_type, var_any_player, 7, 1)))),
        ("not", ((ChessPredicates.PIECE_AT, 
                (var_any_type, var_any_player, 7, 2)))),
        ("not", ((ChessPredicates.PIECE_AT, 
                (var_any_type, var_any_player, 7, 3)))),
        
        # King must not be in check or pass through check
        ("not", ((ChessPredicates.IN_CHECK, 
                (Player.WHITE)))),
        ("not", ((ChessPredicates.SQUARE_ATTACKED, 
                (Player.BLACK, 7, 3)))),
        ("not", ((ChessPredicates.SQUARE_ATTACKED, 
                (Player.BLACK, 7, 2))))
    ]
    
    logic_engine.add_rule(head, body)
    
    # Black queenside castling
    head = (ChessPredicates.CAN_CASTLE, 
            (Player.BLACK, "queenside", 0, 4, 0, 2))
    
    body = [
        # King must not have moved
        (ChessPredicates.HAS_MOVED, 
         (PieceType.KING, Player.BLACK, 0, 4, False)),
        
        # Rook must be present and not have moved
        (ChessPredicates.PIECE_AT, 
         (PieceType.ROOK, Player.BLACK, 0, 0)),
        (ChessPredicates.HAS_MOVED, 
         (PieceType.ROOK, Player.BLACK, 0, 0, False)),
        
        # Squares between king and rook must be empty
        ("not", ((ChessPredicates.PIECE_AT, 
                (var_any_type, var_any_player, 0, 1)))),
        ("not", ((ChessPredicates.PIECE_AT, 
                (var_any_type, var_any_player, 0, 2)))),
        ("not", ((ChessPredicates.PIECE_AT, 
                (var_any_type, var_any_player, 0, 3)))),
        
        # King must not be in check or pass through check
        ("not", ((ChessPredicates.IN_CHECK, 
                (Player.BLACK)))),
        ("not", ((ChessPredicates.SQUARE_ATTACKED, 
                (Player.WHITE, 0, 3)))),
        ("not", ((ChessPredicates.SQUARE_ATTACKED, 
                (Player.WHITE, 0, 2))))
    ]
    
    logic_engine.add_rule(head, body)
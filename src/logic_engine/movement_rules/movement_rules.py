"""
Main movement rules module for the chess logic engine.
Defines the general movement predicates and queries.
"""

from src.logic.piece_type import PieceType
from src.logic_engine.predicates import ChessPredicates
from src.logic_engine.movement_rules.blocking_rules import setup_blocking_rules
from src.logic_engine.movement_rules.pawn_rules import setup_pawn_rules
from src.logic_engine.movement_rules.knight_rules import setup_knight_rules
from src.logic_engine.movement_rules.bishop_rules import setup_bishop_rules
from src.logic_engine.movement_rules.rook_rules import setup_rook_rules
from src.logic_engine.movement_rules.queen_rules import setup_queen_rules
from src.logic_engine.movement_rules.king_rules import setup_king_rules


def setup_movement_rules(logic_engine):
    """
    Setup all movement rules in the logic engine.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Setup blocking rules
    setup_blocking_rules(logic_engine)
    
    # Setup piece-specific movement rules
    setup_pawn_rules(logic_engine)
    setup_knight_rules(logic_engine)
    setup_bishop_rules(logic_engine)
    setup_rook_rules(logic_engine)
    setup_queen_rules(logic_engine)
    setup_king_rules(logic_engine)
    
    # Setup general can_move rule that combines movement and capture
    setup_can_move_rule(logic_engine)


def setup_can_move_rule(logic_engine):
    """
    Setup the general can_move rule that combines movement and capture.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Basic can_move rule for empty target square
    # can_move(Type, Player, FromRow, FromCol, ToRow, ToCol) :-
    #     piece_at(Type, Player, FromRow, FromCol),
    #     piece_move(Type, Player, FromRow, FromCol, ToRow, ToCol),
    #     not(piece_at(_, _, ToRow, ToCol)).
    
    var_type = logic_engine.variable("Type")
    var_player = logic_engine.variable("Player")
    var_from_row = logic_engine.variable("FromRow")
    var_from_col = logic_engine.variable("FromCol")
    var_to_row = logic_engine.variable("ToRow")
    var_to_col = logic_engine.variable("ToCol")
    var_any_type = logic_engine.variable("AnyType")
    var_any_player = logic_engine.variable("AnyPlayer")
    
    head = (ChessPredicates.CAN_MOVE, 
            (var_type, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        (ChessPredicates.PIECE_AT, 
         (var_type, var_player, var_from_row, var_from_col)),
        (ChessPredicates.PIECE_MOVE, 
         (var_type, var_player, var_from_row, var_from_col, var_to_row, var_to_col)),
        ("not", 
         ((ChessPredicates.PIECE_AT, 
           (var_any_type, var_any_player, var_to_row, var_to_col))))
    ]
    
    logic_engine.add_rule(head, body)
    
    # Can_move rule for capturing opponent's piece
    # can_move(Type, Player, FromRow, FromCol, ToRow, ToCol) :-
    #     piece_at(Type, Player, FromRow, FromCol),
    #     piece_capture(Type, Player, FromRow, FromCol, ToRow, ToCol),
    #     piece_at(_, OpponentPlayer, ToRow, ToCol),
    #     Player != OpponentPlayer.
    
    var_opponent = logic_engine.variable("OpponentPlayer")
    
    head = (ChessPredicates.CAN_MOVE, 
            (var_type, var_player, var_from_row, var_from_col, var_to_row, var_to_col))
    
    body = [
        (ChessPredicates.PIECE_AT, 
         (var_type, var_player, var_from_row, var_from_col)),
        (ChessPredicates.PIECE_CAPTURE, 
         (var_type, var_player, var_from_row, var_from_col, var_to_row, var_to_col)),
        (ChessPredicates.PIECE_AT, 
         (var_any_type, var_opponent, var_to_row, var_to_col)),
        ("not_equal", (var_player, var_opponent))
    ]
    
    logic_engine.add_rule(head, body)


def can_move_query(logic_engine, piece_type, player, from_row, from_col, to_row=None, to_col=None):
    """
    Query for possible moves for a piece.
    
    Args:
        logic_engine: The logic engine to query
        piece_type: The type of piece
        player: The player who owns the piece
        from_row: The current row of the piece
        from_col: The current column of the piece
        to_row: The target row (optional, can be None to find all possible moves)
        to_col: The target column (optional, can be None to find all possible moves)
        
    Returns:
        A list of possible moves as (to_row, to_col) pairs
    """
    var_to_row = logic_engine.variable("ToRow") if to_row is None else to_row
    var_to_col = logic_engine.variable("ToCol") if to_col is None else to_col
    
    results = logic_engine.query(
        ChessPredicates.CAN_MOVE,
        piece_type, player, from_row, from_col, var_to_row, var_to_col)
    
    moves = []
    for binding in results:
        # Extract bound values for row and column
        bound_row = binding.get("ToRow") if to_row is None else to_row
        bound_col = binding.get("ToCol") if to_col is None else to_col
        
        moves.append((bound_row, bound_col))
    
    return moves
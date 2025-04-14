"""
Logic for determining game end conditions.
This module handles all game-ending rules like insufficient material, 
fifty-move rule, and threefold repetition.
"""

from src.logic.piece_type import PieceType
from src.logic.player import Player
from src.logic.end_reason import EndReason
from src.logic_engine.predicates import ChessPredicates


def setup_game_end_conditions(logic_engine):
    """
    Setup all game end condition rules.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    # Setup other game end conditions
    setup_insufficient_material_rules(logic_engine)
    setup_fifty_move_rule(logic_engine)
    setup_threefold_repetition_rule(logic_engine)


def setup_insufficient_material_rules(logic_engine):
    """
    Setup rules for determining insufficient material.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    var_piece_type = logic_engine.variable("PieceType")
    var_player = logic_engine.variable("Player")
    var_row = logic_engine.variable("Row")
    var_col = logic_engine.variable("Col")
    
    # King vs King
    head = (ChessPredicates.INSUFFICIENT_MATERIAL, ())
    
    body = [
        # Check if there are exactly two kings on the board
        ("count_pieces", 
         (PieceType.KING, 2)),
        ("count_total_pieces", (2))
    ]
    
    logic_engine.add_rule(head, body)
    
    # King + Bishop vs King
    head = (ChessPredicates.INSUFFICIENT_MATERIAL, ())
    
    body = [
        # Check if there are exactly three pieces on the board
        ("count_total_pieces", (3)),
        
        # Check if one player has a bishop
        ("or", (
            # White has a bishop
            ("count_pieces_for_player", 
             (Player.WHITE, PieceType.BISHOP, 1)),
            # Black has a bishop
            ("count_pieces_for_player", 
             (Player.BLACK, PieceType.BISHOP, 1))
        ))
    ]
    
    logic_engine.add_rule(head, body)
    
    # King + Knight vs King
    head = (ChessPredicates.INSUFFICIENT_MATERIAL, ())
    
    body = [
        # Check if there are exactly three pieces on the board
        ("count_total_pieces", (3)),
        
        # Check if one player has a knight
        ("or", (
            # White has a knight
            ("count_pieces_for_player", 
             (Player.WHITE, PieceType.KNIGHT, 1)),
            # Black has a knight
            ("count_pieces_for_player", 
             (Player.BLACK, PieceType.KNIGHT, 1))
        ))
    ]
    
    logic_engine.add_rule(head, body)
    
    # King + Bishop vs King + Bishop (same color bishops)
    head = (ChessPredicates.INSUFFICIENT_MATERIAL, ())
    
    body = [
        # Check if there are exactly four pieces on the board
        ("count_total_pieces", (4)),
        
        # Check if both players have a bishop
        ("count_pieces_for_player", 
         (Player.WHITE, PieceType.BISHOP, 1)),
        ("count_pieces_for_player", 
         (Player.BLACK, PieceType.BISHOP, 1)),
        
        # Check if bishops are on same color squares
        ("bishops_on_same_color", ())
    ]
    
    logic_engine.add_rule(head, body)


def setup_fifty_move_rule(logic_engine):
    """
    Setup rule for fifty-move rule.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    var_count = logic_engine.variable("Count")
    
    # Fifty-move rule: 50 moves without a pawn move or capture
    head = (ChessPredicates.FIFTY_MOVE_RULE, ())
    
    body = [
        # Check if the count of moves without pawn move or capture is 100 (50 full moves)
        ("no_capture_or_pawn_move_count", (var_count)),
        ("equal", (var_count, 100))
    ]
    
    logic_engine.add_rule(head, body)


def setup_threefold_repetition_rule(logic_engine):
    """
    Setup rule for threefold repetition.
    
    Args:
        logic_engine: The logic engine to add rules to
    """
    var_position = logic_engine.variable("Position")
    var_count = logic_engine.variable("Count")
    
    # Threefold repetition: same position occurs three times
    head = (ChessPredicates.THREEFOLD_REPETITION, ())
    
    body = [
        # Check if any position has occurred three times
        ("position_count", (var_position, var_count)),
        ("greater_than_or_equal", (var_count, 3))
    ]
    
    logic_engine.add_rule(head, body)


def register_game_end_handlers(logic_engine):
    """
    Register the handlers for game end condition predicates.
    
    Args:
        logic_engine: The logic engine to register handlers with
    """
    # Register handlers for piece counting
    def count_pieces(args, bindings):
        piece_type = args[0]
        expected_count = args[1]
        
        var_player = logic_engine.variable("Player")
        var_row = logic_engine.variable("Row")
        var_col = logic_engine.variable("Col")
        
        # Count pieces of the specified type
        results = logic_engine.query(
            ChessPredicates.PIECE_AT,
            piece_type, var_player, var_row, var_col
        )
        
        return len(results) == expected_count
    
    # Register handler for total piece count
    def count_total_pieces(args, bindings):
        expected_count = args[0]
        
        var_type = logic_engine.variable("Type")
        var_player = logic_engine.variable("Player")
        var_row = logic_engine.variable("Row")
        var_col = logic_engine.variable("Col")
        
        # Count all pieces
        results = logic_engine.query(
            ChessPredicates.PIECE_AT,
            var_type, var_player, var_row, var_col
        )
        
        return len(results) == expected_count
    
    # Register handler for counting pieces for a specific player
    def count_pieces_for_player(args, bindings):
        player = args[0]
        piece_type = args[1]
        expected_count = args[2]
        
        var_row = logic_engine.variable("Row")
        var_col = logic_engine.variable("Col")
        
        # Count pieces of the specified type for the player
        results = logic_engine.query(
            ChessPredicates.PIECE_AT,
            piece_type, player, var_row, var_col
        )
        
        return len(results) == expected_count
    
    # Register handler to check if bishops are on the same color squares
    def bishops_on_same_color(args, bindings):
        var_row = logic_engine.variable("Row")
        var_col = logic_engine.variable("Col")
        
        # Find white bishop position
        white_bishop_results = logic_engine.query(
            ChessPredicates.PIECE_AT,
            PieceType.BISHOP, Player.WHITE, var_row, var_col
        )
        
        # Find black bishop position
        black_bishop_results = logic_engine.query(
            ChessPredicates.PIECE_AT,
            PieceType.BISHOP, Player.BLACK, var_row, var_col
        )
        
        if not white_bishop_results or not black_bishop_results:
            return False
        
        # Get bishop positions
        white_bishop_binding = white_bishop_results[0]
        black_bishop_binding = black_bishop_results[0]
        
        white_bishop_row = white_bishop_binding.get("Row")
        white_bishop_col = white_bishop_binding.get("Col")
        black_bishop_row = black_bishop_binding.get("Row")
        black_bishop_col = black_bishop_binding.get("Col")
        
        # Check if both bishops are on the same color squares
        white_square_color = (white_bishop_row + white_bishop_col) % 2
        black_square_color = (black_bishop_row + black_bishop_col) % 2
        
        return white_square_color == black_square_color
    
    # Register handlers with the logic engine
    logic_engine.register_predicate_handler("count_pieces", count_pieces)
    logic_engine.register_predicate_handler("count_total_pieces", count_total_pieces)
    logic_engine.register_predicate_handler("count_pieces_for_player", count_pieces_for_player)
    logic_engine.register_predicate_handler("bishops_on_same_color", bishops_on_same_color)
"""
Functions for executing special moves.
"""

from src.logic_engine.piece_type import PieceType
from src.logic_engine.player import Player
from src.logic_engine.predicates import ChessPredicates


def execute_castle(logic_engine, player, castle_side, from_row, from_col, to_row, to_col):
    """
    Execute a castling move.
    
    Args:
        logic_engine: The logic engine
        player: The player making the move
        castle_side: "kingside" or "queenside"
        from_row: King's starting row
        from_col: King's starting column (usually 4)
        to_row: King's ending row
        to_col: King's ending column (6 for kingside, 2 for queenside)
    """
    # Determine rook's starting and ending positions
    if castle_side == "kingside":
        rook_from_col = 7
        rook_to_col = 5
    else:  # queenside
        rook_from_col = 0
        rook_to_col = 3
    
    # Move the king
    move_piece(logic_engine, PieceType.KING, player, from_row, from_col, to_row, to_col)
    
    # Move the rook
    move_piece(logic_engine, PieceType.ROOK, player, from_row, rook_from_col, to_row, rook_to_col)


def execute_en_passant(logic_engine, player, from_row, from_col, to_row, to_col):
    """
    Execute an en passant capture.
    
    Args:
        logic_engine: The logic engine
        player: The player making the move
        from_row: Pawn's starting row
        from_col: Pawn's starting column
        to_row: Pawn's ending row
        to_col: Pawn's ending column
    """
    # Find the captured pawn's position
    capture_row = from_row
    capture_col = to_col
    opponent = Player.BLACK if player == Player.WHITE else Player.WHITE
    
    # Move the capturing pawn
    move_piece(logic_engine, PieceType.PAWN, player, from_row, from_col, to_row, to_col)
    
    # Remove the captured pawn
    remove_piece(logic_engine, capture_row, capture_col)
    
    # Clear the pawn_skip fact
    var_any_row = logic_engine.variable("AnyRow")
    var_any_col = logic_engine.variable("AnyCol")
    
    results = logic_engine.query(
        ChessPredicates.PAWN_SKIP,
        opponent, var_any_row, var_any_col
    )
    
    for binding in results:
        row = binding.get("AnyRow")
        col = binding.get("AnyCol")
        logic_engine.retract_fact(
            ChessPredicates.PAWN_SKIP,
            opponent, row, col
        )


def execute_promotion(logic_engine, player, from_row, from_col, to_row, to_col, new_type):
    """
    Execute a pawn promotion.
    
    Args:
        logic_engine: The logic engine
        player: The player making the move
        from_row: Pawn's starting row
        from_col: Pawn's starting column
        to_row: Pawn's ending row
        to_col: Pawn's ending column
        new_type: The type of piece to promote to
    """
    # Check if there's a capture
    var_any_type = logic_engine.variable("AnyType")
    var_any_player = logic_engine.variable("AnyPlayer")
    
    results = logic_engine.query(
        ChessPredicates.PIECE_AT,
        var_any_type, var_any_player, to_row, to_col
    )
    
    # Remove the captured piece if any
    if results:
        remove_piece(logic_engine, to_row, to_col)
    
    # Remove the pawn
    remove_piece(logic_engine, from_row, from_col)
    
    # Add the new piece
    logic_engine.assert_fact(
        ChessPredicates.PIECE_AT,
        new_type, player, to_row, to_col
    )
    
    # Mark the new piece as having moved
    logic_engine.assert_fact(
        ChessPredicates.HAS_MOVED,
        new_type, player, to_row, to_col, True
    )


def move_piece(logic_engine, piece_type, player, from_row, from_col, to_row, to_col):
    """
    Move a piece from one position to another.
    
    Args:
        logic_engine: The logic engine
        piece_type: The type of piece
        player: The player who owns the piece
        from_row: Starting row
        from_col: Starting column
        to_row: Ending row
        to_col: Ending column
    """
    # Check if there's a capture
    var_any_type = logic_engine.variable("AnyType")
    var_any_player = logic_engine.variable("AnyPlayer")
    
    results = logic_engine.query(
        ChessPredicates.PIECE_AT,
        var_any_type, var_any_player, to_row, to_col
    )
    
    # Remove the captured piece if any
    if results:
        remove_piece(logic_engine, to_row, to_col)
    
    # Remove piece from original position
    logic_engine.retract_fact(
        ChessPredicates.PIECE_AT,
        piece_type, player, from_row, from_col
    )
    
    # Get has_moved status
    var_has_moved = logic_engine.variable("HasMoved")
    moved_results = logic_engine.query(
        ChessPredicates.HAS_MOVED,
        piece_type, player, from_row, from_col, var_has_moved
    )
    
    # Remove old has_moved fact
    if moved_results:
        binding = moved_results[0]
        has_moved = binding.get("HasMoved")
        logic_engine.retract_fact(
            ChessPredicates.HAS_MOVED,
            piece_type, player, from_row, from_col, has_moved
        )
    
    # Add piece to new position
    logic_engine.assert_fact(
        ChessPredicates.PIECE_AT,
        piece_type, player, to_row, to_col
    )
    
    # Mark piece as having moved
    logic_engine.assert_fact(
        ChessPredicates.HAS_MOVED,
        piece_type, player, to_row, to_col, True
    )


def remove_piece(logic_engine, row, col):
    """
    Remove a piece from the board.
    
    Args:
        logic_engine: The logic engine
        row: The row of the piece
        col: The column of the piece
    """
    var_type = logic_engine.variable("Type")
    var_player = logic_engine.variable("Player")
    var_has_moved = logic_engine.variable("HasMoved")
    
    # Get piece information
    piece_results = logic_engine.query(
        ChessPredicates.PIECE_AT,
        var_type, var_player, row, col
    )
    
    if not piece_results:
        return
    
    # Get piece type and player
    binding = piece_results[0]
    piece_type = binding.get("Type")
    player = binding.get("Player")
    
    # Remove piece_at fact
    logic_engine.retract_fact(
        ChessPredicates.PIECE_AT,
        piece_type, player, row, col
    )
    
    # Remove has_moved fact
    moved_results = logic_engine.query(
        ChessPredicates.HAS_MOVED,
        piece_type, player, row, col, var_has_moved
    )
    
    if moved_results:
        binding = moved_results[0]
        has_moved = binding.get("HasMoved")
        logic_engine.retract_fact(
            ChessPredicates.HAS_MOVED,
            piece_type, player, row, col, has_moved
        )
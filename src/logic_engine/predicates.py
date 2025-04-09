"""
Predicates for the chess game.
Defines the standard predicates used in the logic representation.
"""

# Basic board predicates
# piece_at(Type, Player, Row, Col) - Represents a piece on the board
# current_player(Player) - Indicates which player's turn it is
# has_moved(Type, Player, Row, Col, HasMoved) - Tracks if a piece has moved

# En passant predicates
# pawn_skip(Player, Row, Col) - Represents a position where a pawn has skipped and can be captured by en passant

# Check and checkmate predicates
# in_check(Player) - Indicates that a player is in check
# checkmate(Player) - Indicates that a player is in checkmate
# stalemate(Player) - Indicates that a player is in stalemate

# Move predicates - to be implemented in Commit 3
# can_move(Type, Player, FromRow, FromCol, ToRow, ToCol) - Indicates that a piece can move to a position
# can_capture(Type, Player, FromRow, FromCol, ToRow, ToCol) - Indicates that a piece can capture at a position
# is_blocked(FromRow, FromCol, ToRow, ToCol) - Indicates that a move path is blocked

# Special move predicates - to be implemented in Commit 4
# can_castle(Player, Side) - Indicates that a player can castle on a side (kingside or queenside)
# can_en_passant(Player, FromRow, FromCol, ToRow, ToCol) - Indicates that a pawn can make an en passant capture
# can_promote(Player, FromRow, FromCol, ToRow, ToCol, NewType) - Indicates that a pawn can be promoted

class ChessPredicates:
    """
    Standard predicates for chess logic programming.
    This class simply documents the predicates used in the system.
    """
    
    # Board state predicates
    PIECE_AT = "piece_at"
    CURRENT_PLAYER = "current_player"
    HAS_MOVED = "has_moved"
    PAWN_SKIP = "pawn_skip"
    
    # Game state predicates
    IN_CHECK = "in_check"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    
    # Move predicates
    CAN_MOVE = "can_move"
    CAN_CAPTURE = "can_capture"
    IS_BLOCKED = "is_blocked"
    
    # Special move predicates
    CAN_CASTLE = "can_castle"
    CAN_EN_PASSANT = "can_en_passant"
    CAN_PROMOTE = "can_promote"
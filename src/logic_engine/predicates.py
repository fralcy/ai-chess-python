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

# Movement predicates
# piece_move(Type, Player, FromRow, FromCol, ToRow, ToCol) - Indicates a valid move pattern for a piece
# piece_capture(Type, Player, FromRow, FromCol, ToRow, ToCol) - Indicates a valid capture pattern for a piece
# is_blocked(FromRow, FromCol, ToRow, ToCol) - Indicates that a move path is blocked
# can_move(Type, Player, FromRow, FromCol, ToRow, ToCol) - Indicates that a piece can move to a position

# Check and checkmate predicates
# in_check(Player) - Indicates that a player is in check
# checkmate(Player) - Indicates that a player is in checkmate
# stalemate(Player) - Indicates that a player is in stalemate
# square_attacked(AttackingPlayer, Row, Col) - Indicates that a square is under attack by a player

# Special move predicates
# can_castle(Player, Side, FromRow, FromCol, ToRow, ToCol) - Indicates that a player can castle on a side
# can_en_passant(Player, FromRow, FromCol, ToRow, ToCol) - Indicates that a pawn can make an en passant capture
# can_promote(Player, FromRow, FromCol, ToRow, ToCol, NewType) - Indicates that a pawn can be promoted

# Utility predicates
# opponent(Player, OpponentPlayer) - Gets the opponent of a player

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
    
    # Movement predicates
    PIECE_MOVE = "piece_move"
    PIECE_CAPTURE = "piece_capture"
    IS_BLOCKED = "is_blocked"
    CAN_MOVE = "can_move"
    
    # Game state predicates
    IN_CHECK = "in_check"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    SQUARE_ATTACKED = "square_attacked"
    
    # Special move predicates
    CAN_CASTLE = "can_castle"
    CAN_EN_PASSANT = "can_en_passant"
    CAN_PROMOTE = "can_promote"
    
    # Utility predicates
    OPPONENT = "opponent"
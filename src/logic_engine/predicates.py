"""
Predicates for the chess game.
Defines the standard predicates used in the logic representation.
"""

class ChessPredicates:
    """
    Standard predicates for chess logic programming.
    This class simply documents the predicates used in the system.
    """
    
    # Board state predicates
    PIECE_AT = "piece_at"                 # piece_at(Type, Player, Row, Col)
    CURRENT_PLAYER = "current_player"     # current_player(Player)
    HAS_MOVED = "has_moved"               # has_moved(Type, Player, Row, Col, HasMoved)
    PAWN_SKIP = "pawn_skip"               # pawn_skip(Player, Row, Col)
    
    # Movement predicates
    PIECE_MOVE = "piece_move"             # piece_move(Type, Player, FromRow, FromCol, ToRow, ToCol)
    PIECE_CAPTURE = "piece_capture"       # piece_capture(Type, Player, FromRow, FromCol, ToRow, ToCol)
    IS_BLOCKED = "is_blocked"             # is_blocked(FromRow, FromCol, ToRow, ToCol)
    CAN_MOVE = "can_move"                 # can_move(Type, Player, FromRow, FromCol, ToRow, ToCol)
    
    # Game state predicates
    IN_CHECK = "in_check"                 # in_check(Player)
    CHECKMATE = "checkmate"               # checkmate(Player)
    STALEMATE = "stalemate"               # stalemate(Player)
    SQUARE_ATTACKED = "square_attacked"   # square_attacked(AttackingPlayer, Row, Col)
    NO_LEGAL_MOVES = "no_legal_moves"     # no_legal_moves(Player)
    HAS_LEGAL_MOVE = "has_legal_move"     # has_legal_move(Player)
    LEAVES_IN_CHECK = "leaves_in_check"   # leaves_in_check(Player, PieceType, FromRow, FromCol, ToRow, ToCol)
    MOVE_RESULTS_IN_CHECK = "move_results_in_check"  # move_results_in_check(Player, PieceType, FromRow, FromCol, ToRow, ToCol)
    RESOLVES_CHECK = "resolves_check"     # resolves_check(Player, PieceType, FromRow, FromCol, ToRow, ToCol)
    
    # Game end condition predicates
    INSUFFICIENT_MATERIAL = "insufficient_material"  # insufficient_material()
    FIFTY_MOVE_RULE = "fifty_move_rule"             # fifty_move_rule()
    THREEFOLD_REPETITION = "threefold_repetition"   # threefold_repetition()
    
    # Special move predicates
    CAN_CASTLE = "can_castle"             # can_castle(Player, Side, FromRow, FromCol, ToRow, ToCol)
    CAN_EN_PASSANT = "can_en_passant"     # can_en_passant(Player, FromRow, FromCol, ToRow, ToCol)
    CAN_PROMOTE = "can_promote"           # can_promote(Player, FromRow, FromCol, ToRow, ToCol, NewType)
    
    # Utility predicates
    OPPONENT = "opponent"                 # opponent(Player, OpponentPlayer)
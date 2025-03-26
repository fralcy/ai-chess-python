from enum import Enum, auto

class MoveType(Enum):
    """Enumeration of move types."""
    NORMAL = auto()
    CASTLE_KS = auto()
    CASTLE_QS = auto()
    DOUBLE_PAWN = auto()
    EN_PASSANT = auto()
    PAWN_PROMOTION = auto()
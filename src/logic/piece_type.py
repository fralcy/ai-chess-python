from enum import Enum, auto

class PieceType(Enum):
    """Enumeration of piece types."""
    NONE = auto()
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()
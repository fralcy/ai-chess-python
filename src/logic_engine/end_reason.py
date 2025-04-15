from enum import Enum, auto

class EndReason(Enum):
    """The reason why the game ended."""
    CHECKMATE = auto()
    STALEMATE = auto()
    FIFTY_MOVE_RULE = auto()
    INSUFFICIENT_MATERIAL = auto()
    THREEFOLD_REPETITION = auto()
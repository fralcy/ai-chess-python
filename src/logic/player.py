from enum import Enum, auto

class Player(Enum):
    NONE = auto()
    WHITE = auto()
    BLACK = auto()

    def opponent(self):
        """Return the opponent player."""
        if self == Player.WHITE:
            return Player.BLACK
        elif self == Player.BLACK:
            return Player.WHITE
        else:
            return Player.NONE
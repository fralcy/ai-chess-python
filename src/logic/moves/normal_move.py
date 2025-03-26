from move import Move
from logic.move_type import MoveType
from logic.pieces.piece import Piece

class NormalMove(Move):
    @property
    def type(self):
        return MoveType.NORMAL

    @property
    def from_pos(self):
        return self._from_pos

    @property
    def to_pos(self):
        return self._to_pos
    
    def __init__(self, from_pos, to_pos):
        self._from_pos = from_pos
        self._to_pos = to_pos

    def execute(self, board):
        piece = board[self.from_pos]
        board[self.to_pos] = piece
        board[self.from_pos] = None
        piece.has_moved = True

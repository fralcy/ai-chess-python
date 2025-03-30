from logic.moves.move import Move
from logic.move_type import MoveType
from logic.piece_type import PieceType

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

    def execute(self, board) -> bool:
        piece = board.get_piece(self.from_pos)
        capture = not board.is_empty(self.to_pos)
        board.set_piece(self.to_pos, piece)
        board.set_piece(self.from_pos, None)
        piece.has_moved = True

        return capture or piece.piece_type == PieceType.PAWN

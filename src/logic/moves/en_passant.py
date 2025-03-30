from logic.moves.move import Move
from logic.move_type import MoveType
from logic.position import Position
from logic.moves.normal_move import NormalMove

class EnPassant(Move):
    @property
    def type(self):
        return MoveType.EN_PASSANT
    
    @property
    def from_pos(self):
        return self._from_pos
    
    @property
    def to_pos(self):
        return self._to_pos
    
    @property
    def capture_pos(self):
        return self._capture_pos
    
    def __init__(self, from_pos, to_pos,):
        self._from_pos = from_pos
        self._to_pos = to_pos
        self._capture_pos = Position(from_pos.row, to_pos.column)

    def execute(self, board) -> bool:
        NormalMove(self._from_pos, self._to_pos).execute(board)
        board.set_piece(self._capture_pos, None)

        return True
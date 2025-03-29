from logic.moves.move import Move
from logic.move_type import MoveType
from logic.position import Position
from logic.moves.normal_move import NormalMove

class DoublePawn(Move):
    @property
    def type(self):
        return MoveType.DOUBLE_PAWN
    
    @property
    def from_pos(self):
        return self._from_pos
    
    @property
    def to_pos(self):
        return self._to_pos
    
    @property
    def skipped_pos(self):
        return self._skipped_pos
    
    def __init__(self, from_pos, to_pos):
        self._from_pos = from_pos
        self._to_pos = to_pos
        self._skipped_pos = Position((from_pos.row + to_pos.row) // 2, from_pos.column)

    def execute(self, board):
        player = board.get_piece(self._from_pos).color
        board.set_pawn_skip_position(player, self._skipped_pos)
        NormalMove(self._from_pos, self._to_pos).execute(board)
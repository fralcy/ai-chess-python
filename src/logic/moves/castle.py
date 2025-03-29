from logic.moves.move import Move
from logic.move_type import MoveType
from logic.direction import Direction
from logic.position import Position
from logic.moves.normal_move import NormalMove

class Castle(Move):
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, value):
        self._type = value
    
    @property
    def from_pos(self):
        return self._from_pos
    
    @from_pos.setter
    def from_pos(self, value):
        self._from_pos = value
    
    @property
    def to_pos(self):
        return self._to_pos
    
    @property
    def king_move_direction(self):
        return self._king_move_direction
    
    @property
    def rook_from_pos(self):
        return self._rook_from_pos
    
    @property
    def rook_to_pos(self):
        return self._rook_to_pos
    
    def __init__(self, type: MoveType, king_pos: Position):
        self._type = type
        self._from_pos = king_pos

        if type == MoveType.CASTLE_KS:
            self._king_move_direction = Direction.EAST
            self._to_pos = Position(king_pos.row, 6)
            self._rook_from_pos = Position(king_pos.row, 7)
            self._rook_to_pos = Position(king_pos.row, 5)
        elif type == MoveType.CASTLE_QS:
            self._king_move_direction = Direction.WEST
            self._to_pos = Position(king_pos.row, 2)
            self._rook_from_pos = Position(king_pos.row, 0)
            self._rook_to_pos = Position(king_pos.row, 3)
        else:
            raise ValueError("Invalid castle type")
    
    def execute(self, board):
        NormalMove(self.from_pos, self.to_pos).execute(board);
        NormalMove(self.rook_from_pos, self.rook_to_pos).execute(board)

    def is_legal(self, board):
        player = board.get_piece(self.from_pos).color

        if board.is_in_check(player):
            return False
        
        board_copy = board.copy()
        king_pos_in_copy = self.from_pos

        for i in range(2):
            NormalMove(king_pos_in_copy, king_pos_in_copy + self.king_move_direction).execute(board_copy)
            king_pos_in_copy += self.king_move_direction
            if board_copy.is_in_check(player):
                return False
        
        return True
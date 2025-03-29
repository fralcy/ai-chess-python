from logic.moves.move import Move
from logic.move_type import MoveType
from logic.piece_type import PieceType
from logic.player import Player


class PawnPromotion(Move):
    @property
    def type(self) -> MoveType:
        return MoveType.PAWN_PROMOTION
    
    @property
    def from_pos(self):
        return self._from_pos
    
    @property
    def to_pos(self):
        return self._to_pos
    
    @property
    def new_type(self) -> PieceType:
        return self._new_type
    
    def __init__(self, from_pos, to_pos, new_type: PieceType):
        self._from_pos = from_pos
        self._to_pos = to_pos
        self._new_type = new_type

    def create_promotion_piece(self, color: Player) -> PieceType:
        if self._new_type == PieceType.QUEEN:
            return PieceType.QUEEN
        elif self._new_type == PieceType.ROOK:
            return PieceType.ROOK
        elif self._new_type == PieceType.BISHOP:
            return PieceType.BISHOP
        elif self._new_type == PieceType.KNIGHT:
            return PieceType.KNIGHT
        else:
            raise ValueError("Invalid piece type for promotion.")
        
    def execute(self, board):
        pawn = board.get_piece(self.from_pos)
        board.set_piece(self.from_pos, None)

        new_piece = self.create_promotion_piece(pawn.color)
        new_piece.has_moved = True
        board.set_piece(self.to_pos, new_piece)

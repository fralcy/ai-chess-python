from logic.moves.move import Move
from logic.move_type import MoveType
from logic.piece_type import PieceType
from logic.player import Player
from logic.pieces.queen import Queen
from logic.pieces.rook import Rook
from logic.pieces.bishop import Bishop
from logic.pieces.knight import Knight

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

    def create_promotion_piece(self, color: Player):
        """Create a new piece object based on the promotion type and color."""
        if self._new_type == PieceType.QUEEN:
            return Queen(color)
        elif self._new_type == PieceType.ROOK:
            return Rook(color)
        elif self._new_type == PieceType.BISHOP:
            return Bishop(color)
        elif self._new_type == PieceType.KNIGHT:
            return Knight(color)
        else:
            raise ValueError("Invalid piece type for promotion.")
        
        
    def execute(self, board):
        pawn = board.get_piece(self.from_pos)
        color = pawn.color
        board.set_piece(self.from_pos, None)

        new_piece = self.create_promotion_piece(color)
        new_piece.has_moved = True
        board.set_piece(self.to_pos, new_piece)
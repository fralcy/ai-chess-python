from logic.pieces.piece import Piece
from logic.piece_type import PieceType
from logic.player import Player
from logic.position import Position

class StateString:
    def __init__(self, current_player, board):
        # Initialize a string builder (in Python we can use regular strings)
        self._str = str()
        # Add piece placement data
        self.add_piece_placement(board)
        self._str += " "
        # Add current player
        self.add_current_player(current_player)
        self._str += " "
        # Add castling rights
        self.add_castling_rights(board)
        self._str += " "
        # Add en passant data
        self.add_en_passant(board, current_player)
            
    def __str__(self) -> str:
        return self._str
    
    @staticmethod
    def piece_char(piece) -> str:
        piece_char = str()
        match piece.piece_type:
            case PieceType.PAWN:
                piece_char = "p"
            case PieceType.ROOK:
                piece_char = "r"
            case PieceType.KNIGHT:
                piece_char = "n"
            case PieceType.BISHOP:
                piece_char = "b"
            case PieceType.QUEEN:
                piece_char = "q"
            case PieceType.KING:
                piece_char = "k"
            case _:
                raise ValueError("Unknown piece type")
            
        if piece.color == Player.WHITE:
            return piece_char.upper()
        else:
            return piece_char
        
    def add_row_data(self, board, row):
        empty = 0

        for col in range(8):
            piece = board.get_piece(Position(row, col))
            if piece is None:
                empty += 1
            else:
                if empty > 0:
                    self._str += str(empty)
                    empty = 0
                self._str += self.piece_char(piece)

        if empty > 0:
            self._str += str(empty)

    def add_piece_placement(self, board):
        for row in range(8):
            if row != 0:
                self._str += "/"
            self.add_row_data(board, row)

    def add_current_player(self, current_player):
        if current_player == Player.WHITE:
            self._str += "w"
        else:
            self._str += "b"

    def add_castling_rights(self, board):
        castle_w_ks = board.can_castle_ks(Player.WHITE)
        castle_w_qs = board.can_castle_qs(Player.WHITE)
        castle_b_ks = board.can_castle_ks(Player.BLACK)
        castle_b_qs = board.can_castle_qs(Player.BLACK)

        if not castle_w_ks and not castle_w_qs and not castle_b_ks and not castle_b_qs:
            self._str += "-"
            return
        
        if castle_w_ks:
            self._str += "K"
        if castle_w_qs:
            self._str += "Q"
        if castle_b_ks:
            self._str += "k"
        if castle_b_qs:
            self._str += "q"

    def add_en_passant(self, board, current_player):
        if not board.can_capture_en_passant(current_player):
            self._str += "-"
            return

        pos = board.get_pawn_skip_position(current_player.opponent)
        file = chr("")(ord("a") + pos.col)
        rank = 8 - pos.row
        self._str += file + str(rank)
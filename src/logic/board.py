from logic.player import Player
from logic.pieces import *
from logic.position import Position
from logic.piece_type import PieceType
from logic.pieces.piece import Piece
from logic.counting import Counting
from typing import List
from logic.direction import Direction
from logic.moves.en_passant import EnPassant

class Board:
    def __init__(self):
        self._pieces = [[None for _ in range(8)] for _ in range(8)]
        self.add_starting_pieces()
        self.pawn_skip_positions = {
            Player.WHITE: None,
            Player.BLACK: None
        }

    def get_piece(self, key) -> Piece:
        if isinstance(key, tuple):
            row, col = key
            return self._pieces[row][col]
        else:
            return self._pieces[key.row][key.column]
        
    def set_piece(self, key, value):
        if isinstance(key, tuple):
            row, col = key
            self._pieces[row][col] = value
        else:
            self._pieces[key.row][key.column] = value

    def get_pawn_skip_position(self, player) -> Position:
        return self.pawn_skip_positions[player]
    
    def set_pawn_skip_position(self, player, position):
        self.pawn_skip_positions[player] = position

    def add_starting_pieces(self):
        # Add black pieces
        self._pieces[0][0] = Rook(Player.BLACK)
        self._pieces[0][1] = Knight(Player.BLACK)
        self._pieces[0][2] = Bishop(Player.BLACK)
        self._pieces[0][3] = Queen(Player.BLACK)
        self._pieces[0][4] = King(Player.BLACK)
        self._pieces[0][5] = Bishop(Player.BLACK)
        self._pieces[0][6] = Knight(Player.BLACK)
        self._pieces[0][7] = Rook(Player.BLACK)
        # Add white pieces
        self._pieces[7][0] = Rook(Player.WHITE)
        self._pieces[7][1] = Knight(Player.WHITE)
        self._pieces[7][2] = Bishop(Player.WHITE)
        self._pieces[7][3] = Queen(Player.WHITE)
        self._pieces[7][4] = King(Player.WHITE)
        self._pieces[7][5] = Bishop(Player.WHITE)
        self._pieces[7][6] = Knight(Player.WHITE)
        self._pieces[7][7] = Rook(Player.WHITE)
        # Add pawns
        for i in range(8):
            self._pieces[1][i] = Pawn(Player.BLACK)
            self._pieces[6][i] = Pawn(Player.WHITE)
        return self._pieces
    
    def is_inside(self, pos: Position):
        return 0 <= pos.row < 8 and 0 <= pos.column < 8
    
    def is_empty(self, pos: Position):
        return self.get_piece(pos) is None
    
    def piece_positions(self):
        positions = []
        for row in range(8):
            for col in range(8):
                piece = self._pieces[row][col]
                if piece:
                    positions.append(Position(row, col))
        return positions
    
    def piece_positions_for(self, player):
        return [pos for pos in self.piece_positions() if self.get_piece(pos).color == player]
    
    def is_in_check(self, player):        
        # Check if any opponent piece can capture the king
        opponent = player.opponent()
        for pos in self.piece_positions_for(opponent):
            piece = self.get_piece(pos)
            if piece.can_capture_opponent_king(pos, self):
                return True
        
        return False
    
    def copy(self):
        board_copy = Board()
        # Clear the default pieces
        board_copy._pieces = [[None for _ in range(8)] for _ in range(8)]
        
        # Copy each piece
        for row in range(8):
            for col in range(8):
                piece = self._pieces[row][col]
                if piece:
                    board_copy._pieces[row][col] = piece.copy()
        
        return board_copy
    
    def count_pieces(self) -> Counting:
        counting = Counting()
        for pos in self.piece_positions():
            piece = self.get_piece(pos)
            counting.increment(piece.color, piece.piece_type)
        
        return counting
    
    def insufficient_material(self) -> bool:
        counting = self.count_pieces()

        return self.is_king_vs_king(counting) or \
               self.is_king_and_bishop_vs_king(counting) or \
                self.is_king_and_knight_vs_king(counting) or \
                self.is_king_and_bishop_vs_king_and_bishop(counting)

    @staticmethod
    def  is_king_vs_king(counting: Counting) -> bool:
        return counting.total_count == 2
    
    @staticmethod
    def is_king_and_bishop_vs_king(counting: Counting) -> bool:
        return counting.total_count == 3 and (counting.White(PieceType.BISHOP) == 1 or counting.Black(PieceType.BISHOP) == 1)
    
    @staticmethod
    def is_king_and_knight_vs_king(counting: Counting) -> bool:
        return counting.total_count == 3 and (counting.White(PieceType.KNIGHT) == 1 or counting.Black(PieceType.KNIGHT) == 1)
    
    def is_king_and_bishop_vs_king_and_bishop(self, counting: Counting) -> bool:
        if counting.total_count != 4:
            return False
        if counting.White(PieceType.BISHOP) != 1 and counting.Black(PieceType.BISHOP) != 1:
            return False
        w_bishop_pos = self.find_piece(Player.WHITE, PieceType.BISHOP)
        b_bishop_pos = self.find_piece(Player.BLACK, PieceType.BISHOP)

        return w_bishop_pos.square_color() == b_bishop_pos.square_color()
        
    def find_piece(self, color: Player, piece_type: PieceType) -> Position:
        for pos in self.piece_positions_for(color):
            piece = self.get_piece(pos)
            if piece.piece_type == piece_type:
                return pos
        return None
    
    def is_unmoved_king_and_rook(self, king_pos: Position, rook_pos: Position) -> bool:
        if self.is_empty(king_pos) or self.is_empty(rook_pos):
            return False
        
        king = self.get_piece(king_pos)
        rook = self.get_piece(rook_pos)

        return king.piece_type == PieceType.KING and \
               rook.piece_type == PieceType.ROOK and \
               not king.has_moved and \
               not rook.has_moved
    
    def can_castle_ks(self, player: Player) -> bool:
        if player == Player.WHITE:
            return self.is_unmoved_king_and_rook(Position(7, 4), Position(7, 7))
        else:
            return self.is_unmoved_king_and_rook(Position(0, 4), Position(0, 7))
    
    def can_castle_qs(self, player: Player) -> bool:
        if player == Player.WHITE:
            return self.is_unmoved_king_and_rook(Position(7, 4), Position(7, 0))
        else:
            return self.is_unmoved_king_and_rook(Position(0, 4), Position(0, 0))
    
    def has_pawn_in_position(self, player: Player, pawn_positions: List[Position], skip_pos:Position) -> bool:
        for pos in pawn_positions:
            piece = self.get_piece(pos)
            if piece is None or piece.color != player or piece.piece_type != PieceType.PAWN:
                continue

            move = EnPassant(pos, skip_pos)
            if move.is_legal(self):
                return True
            
        return False

    def can_capture_en_passant(self, player: Player) -> bool:
        skip_pos = self.get_pawn_skip_position(player.opponent())

        if skip_pos is None:
            return False
        
        pawn_positions: List[Position] = []
        if player == Player.WHITE:
            pawn_positions.append(skip_pos + Direction.SOUTH_WEST)
            pawn_positions.append(skip_pos + Direction.SOUTH_EAST)
            
        else:
            pawn_positions.append(skip_pos + Direction.NORTH_WEST)
            pawn_positions.append(skip_pos + Direction.NORTH_EAST)

        return self.has_pawn_in_position(player, pawn_positions, skip_pos)
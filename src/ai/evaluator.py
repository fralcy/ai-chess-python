from logic.board import Board
from logic.player import Player
from logic.piece_type import PieceType
from logic.position import Position

class BoardEvaluator:
    """Evaluates the board position and returns a score from the perspective of the given player."""
    
    # Piece values (standard chess piece values)
    PIECE_VALUES = {
        PieceType.PAWN: 100,
        PieceType.KNIGHT: 320,
        PieceType.BISHOP: 330,
        PieceType.ROOK: 500,
        PieceType.QUEEN: 900,
        PieceType.KING: 20000  # King is extremely valuable
    }
    
    # Piece-Square tables for positional evaluation
    # These tables encourage pieces to move to good squares
    # Values are from white's perspective - will be flipped for black
    
    # Pawns are encouraged to advance and control the center
    PAWN_TABLE = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]
    ]
    
    # Knights are encouraged to stay near the center and avoid the edges
    KNIGHT_TABLE = [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ]
    
    # Bishops are encouraged to control diagonals and stay away from corners
    BISHOP_TABLE = [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5,  5,  5,  5,  5,-10],
        [-10,  0,  5,  0,  0,  5,  0,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ]
    
    # Rooks are encouraged to control open files and 7th rank
    ROOK_TABLE = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]
    ]
    
    # Queens combine the power of rooks and bishops
    QUEEN_TABLE = [
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [-5,  0,  5,  5,  5,  5,  0, -5],
        [0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]
    ]
    
    # Kings are encouraged to stay protected in the corners in the midgame
    KING_TABLE_MIDGAME = [
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [20, 30, 10,  0,  0, 10, 30, 20]
    ]
    
    # Kings are encouraged to move to the center in the endgame
    KING_TABLE_ENDGAME = [
        [-50,-40,-30,-20,-20,-30,-40,-50],
        [-30,-20,-10,  0,  0,-10,-20,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-30,  0,  0,  0,  0,-30,-30],
        [-50,-30,-30,-30,-30,-30,-30,-50]
    ]
    
    @classmethod
    def get_piece_square_table(cls, piece_type, position, board, is_endgame=False):
        """Get the position value from the appropriate piece-square table."""
        row, col = position.row, position.column
        
        # Reverse row index for black pieces
        if board.get_piece(position) and board.get_piece(position).color == Player.BLACK:
            row = 7 - row
        
        if piece_type == PieceType.PAWN:
            return cls.PAWN_TABLE[row][col]
        elif piece_type == PieceType.KNIGHT:
            return cls.KNIGHT_TABLE[row][col]
        elif piece_type == PieceType.BISHOP:
            return cls.BISHOP_TABLE[row][col]
        elif piece_type == PieceType.ROOK:
            return cls.ROOK_TABLE[row][col]
        elif piece_type == PieceType.QUEEN:
            return cls.QUEEN_TABLE[row][col]
        elif piece_type == PieceType.KING:
            if is_endgame:
                return cls.KING_TABLE_ENDGAME[row][col]
            else:
                return cls.KING_TABLE_MIDGAME[row][col]
        return 0
    
    @classmethod
    def count_material(cls, board, player):
        """Count the total material value for a player."""
        total = 0
        for row in range(8):
            for col in range(8):
                pos = Position(row, col)
                piece = board.get_piece(pos)
                if piece and piece.color == player:
                    total += cls.PIECE_VALUES[piece.piece_type]
        return total
    
    @classmethod
    def evaluate(cls, board, player, is_endgame=False):
        """Evaluate the board from perspective of the given player."""
        # If player is in checkmate, return worst possible score
        # If opponent is in checkmate, return best possible score
        opponent = player.opponent()
        
        # Material difference
        player_material = cls.count_material(board, player)
        opponent_material = cls.count_material(board, opponent)
        material_score = player_material - opponent_material
        
        # Positional score
        positional_score = 0
        for row in range(8):
            for col in range(8):
                pos = Position(row, col)
                piece = board.get_piece(pos)
                if not piece:
                    continue
                
                position_value = cls.get_piece_square_table(piece.piece_type, pos, board, is_endgame)
                if piece.color == player:
                    positional_score += position_value
                else:
                    positional_score -= position_value
        
        # Check for checkmate and stalemate
        # This requires a game state which we don't have here
        # Will be added when integrating with the game logic
        
        # Return total score
        return material_score + positional_score * 0.1  # Weight positional score less
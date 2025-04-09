"""
Adapter for converting between traditional Board and LogicBoard.
Provides methods to convert between object-oriented and logic representations.
"""

from src.logic.board import Board
from src.logic.position import Position
from src.logic.player import Player
from src.logic_engine.logic_board import LogicBoard
from src.logic.pieces import Pawn, Knight, Bishop, Rook, Queen, King


class BoardAdapter:
    """
    Adapter for converting between traditional Board and LogicBoard.
    """
    
    def __init__(self, logic_engine=None):
        """
        Initialize the board adapter.
        
        Args:
            logic_engine: An existing LogicEngine instance, or None to create a new one
        """
        self.logic_board = LogicBoard(logic_engine)
    
    def convert_to_logic(self, board):
        """
        Convert a traditional Board object to logical representation.
        
        Args:
            board: A Board object
        """
        self.logic_board.sync_from_board(board)
    
    def convert_to_traditional(self):
        """
        Convert the logical representation to a traditional Board object.
        
        Returns:
            A Board object
        """
        board = Board()
        
        # Clear the default pieces
        board._pieces = [[None for _ in range(8)] for _ in range(8)]
        
        # Get all pieces from logic board
        var_type = self.logic_board.engine.variable("Type")
        var_player = self.logic_board.engine.variable("Player")
        var_row = self.logic_board.engine.variable("Row")
        var_col = self.logic_board.engine.variable("Col")
        
        results = self.logic_board.engine.query(
            "piece_at", var_type, var_player, var_row, var_col)
        
        # Place pieces on the board
        for binding in results:
            piece_type = binding.get("Type")
            player = binding.get("Player")
            row = binding.get("Row")
            col = binding.get("Col")
            
            # Create the appropriate piece
            piece = self._create_piece(piece_type, player)
            
            # Check if the piece has moved
            var_moved = self.logic_board.engine.variable("Moved")
            moved_results = self.logic_board.engine.query(
                "has_moved", piece_type, player, row, col, var_moved)
            
            if moved_results and moved_results[0].get("Moved"):
                piece.has_moved = True
            
            # Set the piece on the board
            board.set_piece((row, col), piece)
        
        # Set pawn skip positions
        var_player = self.logic_board.engine.variable("Player")
        var_row = self.logic_board.engine.variable("Row")
        var_col = self.logic_board.engine.variable("Col")
        
        skip_results = self.logic_board.engine.query(
            "pawn_skip", var_player, var_row, var_col)
        
        for binding in skip_results:
            player = binding.get("Player")
            row = binding.get("Row")
            col = binding.get("Col")
            
            board.set_pawn_skip_position(player, Position(row, col))
        
        return board
    
    def _create_piece(self, piece_type, player):
        """
        Create a piece object based on type and player.
        
        Args:
            piece_type: The type of the piece
            player: The player that owns the piece
            
        Returns:
            A Piece object
        """
        from src.logic.piece_type import PieceType
        
        if piece_type == PieceType.PAWN:
            return Pawn(player)
        elif piece_type == PieceType.KNIGHT:
            return Knight(player)
        elif piece_type == PieceType.BISHOP:
            return Bishop(player)
        elif piece_type == PieceType.ROOK:
            return Rook(player)
        elif piece_type == PieceType.QUEEN:
            return Queen(player)
        elif piece_type == PieceType.KING:
            return King(player)
        
        return None
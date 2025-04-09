"""
Logic-based implementation of the chess board.
Extends the original Board class with logic programming capabilities.
"""

from src.logic.board import Board
from src.logic_engine.board_adapter import BoardAdapter
from src.logic_engine.logic_board import LogicBoard
from src.logic.position import Position


class LogicBasedBoard(Board):
    """
    A chess board implementation that uses logic programming under the hood.
    Extends the traditional Board class but uses logic programming for its operations.
    """
    
    def __init__(self):
        """Initialize the board with both traditional and logic representations."""
        super().__init__()  # Initialize using the traditional way
        
        # Create logic adapter and sync from the traditional board
        self.adapter = BoardAdapter()
        self.adapter.convert_to_logic(self)
    
    def get_piece(self, key):
        """
        Override to use logic representation for getting a piece.
        
        Args:
            key: The position or (row, col) tuple
            
        Returns:
            The piece at the position, or None if empty
        """
        if isinstance(key, tuple):
            row, col = key
            pos = Position(row, col)
        else:
            pos = key
        
        piece_info = self.adapter.logic_board.get_piece_at(pos)
        if piece_info:
            piece_type, player = piece_info
            return self.adapter._create_piece(piece_type, player)
        
        return None
    
    def set_piece(self, key, value):
        """
        Override to use logic representation for setting a piece.
        
        Args:
            key: The position or (row, col) tuple
            value: The piece to set, or None to clear
        """
        # First set using the traditional way
        super().set_piece(key, value)
        
        # Then sync to logic representation
        self.adapter.convert_to_logic(self)
    
    def is_empty(self, pos):
        """
        Override to use logic representation for checking if a square is empty.
        
        Args:
            pos: The position to check
            
        Returns:
            True if the square is empty, False otherwise
        """
        return self.adapter.logic_board.is_square_empty(pos)
    
    def move_piece(self, from_pos, to_pos):
        """
        Move a piece using logic representation.
        
        Args:
            from_pos: The current position of the piece
            to_pos: The destination position
            
        Returns:
            True if the move was successful, False otherwise
        """
        # Use logic representation for the move
        success = self.adapter.logic_board.move_piece(from_pos, to_pos)
        
        # Sync back to traditional representation
        if success:
            traditional_board = self.adapter.convert_to_traditional()
            self._pieces = traditional_board._pieces
            self.pawn_skip_positions = traditional_board.pawn_skip_positions
        
        return success
    
    def set_pawn_skip_position(self, player, position):
        """
        Override to update logic representation when setting pawn skip position.
        
        Args:
            player: The player who made the pawn skip
            position: The position the pawn skipped over
        """
        # First set using the traditional way
        super().set_pawn_skip_position(player, position)
        
        # Then update logic representation
        if position:
            self.adapter.logic_board.engine.assert_fact(
                "pawn_skip", player, position.row, position.column)
        else:
            # Remove existing pawn_skip facts for this player
            var_row = self.adapter.logic_board.engine.variable("Row")
            var_col = self.adapter.logic_board.engine.variable("Col")
            
            results = self.adapter.logic_board.engine.query(
                "pawn_skip", player, var_row, var_col)
            
            for binding in results:
                row = binding.get("Row")
                col = binding.get("Col")
                self.adapter.logic_board.engine.retract_fact(
                    "pawn_skip", player, row, col)
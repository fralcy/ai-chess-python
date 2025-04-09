"""
Logic representation of chess board using predicates.
This module converts the chess board state into logical facts and predicates.
"""

from src.logic.position import Position
from src.logic.player import Player
from src.logic.piece_type import PieceType
from src.logic_engine.engine import LogicEngine


class LogicBoard:
    """
    Represents a chess board as a set of logical facts and rules.
    """
    
    def __init__(self, engine=None):
        """
        Initialize the logical representation of a chess board.
        
        Args:
            engine: An existing LogicEngine instance, or None to create a new one
        """
        self.engine = engine if engine is not None else LogicEngine()
    
    def clear(self):
        """Clear all facts about the board."""
        self.engine.clear()
    
    def setup_initial_board(self):
        """Set up the initial chess position using logical facts."""
        # Clear previous state
        self.clear()
        
        # Current player starts with White
        self.engine.assert_fact("current_player", Player.WHITE)
        
        # Setup white pieces
        self._assert_piece(PieceType.ROOK, Player.WHITE, Position(7, 0))
        self._assert_piece(PieceType.KNIGHT, Player.WHITE, Position(7, 1))
        self._assert_piece(PieceType.BISHOP, Player.WHITE, Position(7, 2))
        self._assert_piece(PieceType.QUEEN, Player.WHITE, Position(7, 3))
        self._assert_piece(PieceType.KING, Player.WHITE, Position(7, 4))
        self._assert_piece(PieceType.BISHOP, Player.WHITE, Position(7, 5))
        self._assert_piece(PieceType.KNIGHT, Player.WHITE, Position(7, 6))
        self._assert_piece(PieceType.ROOK, Player.WHITE, Position(7, 7))
        
        # White pawns
        for col in range(8):
            self._assert_piece(PieceType.PAWN, Player.WHITE, Position(6, col))
        
        # Setup black pieces
        self._assert_piece(PieceType.ROOK, Player.BLACK, Position(0, 0))
        self._assert_piece(PieceType.KNIGHT, Player.BLACK, Position(0, 1))
        self._assert_piece(PieceType.BISHOP, Player.BLACK, Position(0, 2))
        self._assert_piece(PieceType.QUEEN, Player.BLACK, Position(0, 3))
        self._assert_piece(PieceType.KING, Player.BLACK, Position(0, 4))
        self._assert_piece(PieceType.BISHOP, Player.BLACK, Position(0, 5))
        self._assert_piece(PieceType.KNIGHT, Player.BLACK, Position(0, 6))
        self._assert_piece(PieceType.ROOK, Player.BLACK, Position(0, 7))
        
        # Black pawns
        for col in range(8):
            self._assert_piece(PieceType.PAWN, Player.BLACK, Position(1, col))
    
    def _assert_piece(self, piece_type, player, position):
        """
        Assert a piece at a position.
        
        Args:
            piece_type: The type of the piece (PieceType enum)
            player: The player that owns the piece (Player enum)
            position: The position of the piece (Position object)
        """
        self.engine.assert_fact("piece_at", piece_type, player, position.row, position.column)
        self.engine.assert_fact("has_moved", piece_type, player, position.row, position.column, False)
    
    def set_current_player(self, player):
        """
        Set the current player.
        
        Args:
            player: The player to set as current (Player enum)
        """
        # Remove old current player facts
        for old_fact in self.engine.query("current_player", self.engine.variable("Player")):
            player_val = old_fact.get("Player")
            if player_val:
                self.engine.retract_fact("current_player", player_val)
        
        # Add new current player fact
        self.engine.assert_fact("current_player", player)
    
    def get_current_player(self):
        """
        Get the current player.
        
        Returns:
            The current player (Player enum)
        """
        results = self.engine.query("current_player", self.engine.variable("Player"))
        if results:
            return results[0].get("Player")
        return None
    
    def get_piece_at(self, position):
        """
        Get the piece at a position.
        
        Args:
            position: The position to check (Position object)
            
        Returns:
            A tuple (piece_type, player) or None if the square is empty
        """
        var_type = self.engine.variable("Type")
        var_player = self.engine.variable("Player")
        
        results = self.engine.query(
            "piece_at", var_type, var_player, position.row, position.column)
        
        if results:
            binding = results[0]
            piece_type = binding.get("Type")
            player = binding.get("Player")
            return (piece_type, player)
        
        return None
    
    def is_square_empty(self, position):
        """
        Check if a square is empty.
        
        Args:
            position: The position to check (Position object)
            
        Returns:
            True if the square is empty, False otherwise
        """
        return self.get_piece_at(position) is None
    
    def move_piece(self, from_pos, to_pos):
        """
        Move a piece from one position to another.
        
        Args:
            from_pos: The current position of the piece (Position object)
            to_pos: The destination position (Position object)
            
        Returns:
            True if the move was successful, False otherwise
        """
        piece = self.get_piece_at(from_pos)
        if not piece:
            return False
        
        piece_type, player = piece
        
        # Remove any piece at the destination (capture)
        if not self.is_square_empty(to_pos):
            var_type = self.engine.variable("Type")
            var_player = self.engine.variable("Player")
            
            results = self.engine.query(
                "piece_at", var_type, var_player, to_pos.row, to_pos.column)
            
            if results:
                binding = results[0]
                captured_type = binding.get("Type")
                captured_player = binding.get("Player")
                
                self.engine.retract_fact(
                    "piece_at", captured_type, captured_player, 
                    to_pos.row, to_pos.column)
                
                self.engine.retract_fact(
                    "has_moved", captured_type, captured_player,
                    to_pos.row, to_pos.column, True)
        
        # Remove piece from original position
        self.engine.retract_fact(
            "piece_at", piece_type, player, from_pos.row, from_pos.column)
        
        # Remove old has_moved fact
        var_moved = self.engine.variable("Moved")
        results = self.engine.query(
            "has_moved", piece_type, player, from_pos.row, from_pos.column, var_moved)
        
        if results:
            binding = results[0]
            moved = binding.get("Moved")
            self.engine.retract_fact(
                "has_moved", piece_type, player, from_pos.row, from_pos.column, moved)
        
        # Place piece in new position
        self.engine.assert_fact(
            "piece_at", piece_type, player, to_pos.row, to_pos.column)
        
        # Mark as moved
        self.engine.assert_fact(
            "has_moved", piece_type, player, to_pos.row, to_pos.column, True)
        
        # Switch current player
        current_player = self.get_current_player()
        next_player = current_player.opponent()
        self.set_current_player(next_player)
        
        return True
    
    def has_piece_moved(self, position):
        """
        Check if a piece at a position has moved.
        
        Args:
            position: The position to check (Position object)
            
        Returns:
            True if the piece has moved, False otherwise
        """
        piece = self.get_piece_at(position)
        if not piece:
            return False
        
        piece_type, player = piece
        var_moved = self.engine.variable("Moved")
        
        results = self.engine.query(
            "has_moved", piece_type, player, position.row, position.column, var_moved)
        
        if results:
            binding = results[0]
            return binding.get("Moved")
        
        return False
    
    def sync_from_board(self, board):
        """
        Synchronize the logical representation from a regular Board object.
        
        Args:
            board: A Board object to sync from
        """
        self.clear()
        
        # Iterate through all positions on the board
        for row in range(8):
            for col in range(8):
                pos = Position(row, col)
                piece = board.get_piece(pos)
                if piece:
                    self._assert_piece(piece.piece_type, piece.color, pos)
                    if piece.has_moved:
                        # Update has_moved fact
                        self.engine.retract_fact(
                            "has_moved", piece.piece_type, piece.color, row, col, False)
                        self.engine.assert_fact(
                            "has_moved", piece.piece_type, piece.color, row, col, True)
        
        # Set en passant possibility if exists
        for player in [Player.WHITE, Player.BLACK]:
            skip_pos = board.get_pawn_skip_position(player)
            if skip_pos:
                self.engine.assert_fact("pawn_skip", player, skip_pos.row, skip_pos.column)
    
    def setup_rules(self):
        """Set up the rules for the chess game."""
        # Rules for determining valid moves will be added in Commit 3 and 4
        pass
"""
Logic representation of chess board using predicates.
This module converts the chess board state into logical facts and predicates.
"""

from src.logic_engine.position import Position
from src.logic_engine.player import Player
from src.logic_engine.piece_type import PieceType
from src.logic_engine.engine import LogicEngine
from src.logic_engine.predicates import ChessPredicates


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
        
        # Add opponent relationship facts
        self.engine.assert_fact(ChessPredicates.OPPONENT, Player.WHITE, Player.BLACK)
        self.engine.assert_fact(ChessPredicates.OPPONENT, Player.BLACK, Player.WHITE)
    
    def clear(self):
        """Clear all facts about the board."""
        self.engine.clear()
    
    def setup_initial_board(self):
        """Set up the initial chess position using logical facts."""
        # Clear previous state
        self.clear()
        
        # Current player starts with White
        self.engine.assert_fact(ChessPredicates.CURRENT_PLAYER, Player.WHITE)
        
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
        self.engine.assert_fact(ChessPredicates.PIECE_AT, piece_type, player, position.row, position.column)
        self.engine.assert_fact(ChessPredicates.HAS_MOVED, piece_type, player, position.row, position.column, False)
    
    def set_current_player(self, player):
        """
        Set the current player.
        
        Args:
            player: The player to set as current (Player enum)
        """
        # Remove old current player facts
        for old_fact in self.engine.query(ChessPredicates.CURRENT_PLAYER, self.engine.variable("Player")):
            player_val = old_fact.get("Player")
            if player_val:
                self.engine.retract_fact(ChessPredicates.CURRENT_PLAYER, player_val)
        
        # Add new current player fact
        self.engine.assert_fact(ChessPredicates.CURRENT_PLAYER, player)
    
    def get_current_player(self):
        """
        Get the current player.
        
        Returns:
            The current player (Player enum)
        """
        results = self.engine.query(ChessPredicates.CURRENT_PLAYER, self.engine.variable("Player"))
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
            ChessPredicates.PIECE_AT, var_type, var_player, position.row, position.column)
        
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
            ChessPredicates.HAS_MOVED, piece_type, player, position.row, position.column, var_moved)
        
        if results:
            binding = results[0]
            return binding.get("Moved")
        
        return False
    
    def update_piece(self, piece_type, player, position, has_moved=False):
        """
        Update a piece on the board.
        
        Args:
            piece_type: The type of the piece
            player: The player who owns the piece
            position: The position of the piece
            has_moved: Whether the piece has moved
        """
        # Remove any existing piece at this position
        var_type = self.engine.variable("Type")
        var_player = self.engine.variable("Player")
        var_moved = self.engine.variable("Moved")
        
        # Get piece information if exists
        results = self.engine.query(
            ChessPredicates.PIECE_AT, var_type, var_player, position.row, position.column)
        
        if results:
            # Remove existing piece
            binding = results[0]
            old_type = binding.get("Type")
            old_player = binding.get("Player")
            self.engine.retract_fact(ChessPredicates.PIECE_AT, old_type, old_player, position.row, position.column)
            
            # Also remove has_moved fact
            moved_results = self.engine.query(
                ChessPredicates.HAS_MOVED, old_type, old_player, position.row, position.column, var_moved)
                
            if moved_results:
                old_moved = moved_results[0].get("Moved")
                self.engine.retract_fact(ChessPredicates.HAS_MOVED, old_type, old_player, position.row, position.column, old_moved)
        
        # Add the new piece
        self.engine.assert_fact(ChessPredicates.PIECE_AT, piece_type, player, position.row, position.column)
        self.engine.assert_fact(ChessPredicates.HAS_MOVED, piece_type, player, position.row, position.column, has_moved)
    
    def move_piece(self, from_pos, to_pos):
        """
        Move a piece from one position to another.
        
        Args:
            from_pos: The current position of the piece
            to_pos: The destination position
            
        Returns:
            True if the move was successful, False otherwise
        """
        piece = self.get_piece_at(from_pos)
        if not piece:
            return False
        
        piece_type, player = piece
        
        # Check for a capture (piece at destination)
        capture_piece = self.get_piece_at(to_pos)
        
        # Remove the piece from its current position
        self.engine.retract_fact(
            ChessPredicates.PIECE_AT, 
            piece_type, player, from_pos.row, from_pos.column)
        
        # Get has_moved status
        var_moved = self.engine.variable("Moved")
        moved_results = self.engine.query(
            ChessPredicates.HAS_MOVED,
            piece_type, player, from_pos.row, from_pos.column, var_moved
        )
        
        # Remove old has_moved fact
        has_moved = False
        if moved_results:
            binding = moved_results[0]
            has_moved = binding.get("Moved")
            self.engine.retract_fact(
                ChessPredicates.HAS_MOVED,
                piece_type, player, from_pos.row, from_pos.column, has_moved
            )
        
        # Add piece to new position
        self.engine.assert_fact(
            ChessPredicates.PIECE_AT,
            piece_type, player, to_pos.row, to_pos.column
        )
        
        # Mark piece as having moved
        self.engine.assert_fact(
            ChessPredicates.HAS_MOVED,
            piece_type, player, to_pos.row, to_pos.column, True
        )
        
        # Update current player
        current_player = self.get_current_player()
        next_player = Player.BLACK if current_player == Player.WHITE else Player.WHITE
        self.set_current_player(next_player)
        
        return True
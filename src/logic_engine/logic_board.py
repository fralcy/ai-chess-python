"""
Logic representation of chess board using predicates.
This module converts the chess board state into logical facts and predicates.
"""

from src.logic.position import Position
from src.logic.player import Player
from src.logic.piece_type import PieceType
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
        
        # Check for special moves
        from src.logic_engine.special_moves.execute_special_moves import (
            execute_castle, execute_en_passant, execute_promotion, move_piece as execute_move)
        
        # Check for castling
        var_side = self.engine.variable("Side")
        castle_results = self.engine.query(
            ChessPredicates.CAN_CASTLE,
            player, var_side, from_pos.row, from_pos.column, to_pos.row, to_pos.column
        )
        
        if castle_results:
            # Execute castling move
            castle_side = castle_results[0].get("Side")
            execute_castle(self.engine, player, castle_side, 
                        from_pos.row, from_pos.column, to_pos.row, to_pos.column)
            
            # Switch current player
            current_player = self.get_current_player()
            next_player = current_player.opponent()
            self.set_current_player(next_player)
            
            return True
        
        # Check for en passant
        en_passant_results = self.engine.query(
            ChessPredicates.CAN_EN_PASSANT,
            player, from_pos.row, from_pos.column, to_pos.row, to_pos.column
        )
        
        if en_passant_results:
            # Execute en passant capture
            execute_en_passant(self.engine, player, 
                            from_pos.row, from_pos.column, to_pos.row, to_pos.column)
            
            # Switch current player
            current_player = self.get_current_player()
            next_player = current_player.opponent()
            self.set_current_player(next_player)
            
            return True
        
        # Check for promotion
        var_new_type = self.engine.variable("NewType")
        promotion_results = self.engine.query(
            ChessPredicates.CAN_PROMOTE,
            player, from_pos.row, from_pos.column, to_pos.row, to_pos.column, var_new_type
        )
        
        if promotion_results:
            # Default to queen promotion
            new_type = promotion_results[0].get("NewType")
            execute_promotion(self.engine, player, 
                            from_pos.row, from_pos.column, to_pos.row, to_pos.column, new_type)
            
            # Switch current player
            current_player = self.get_current_player()
            next_player = current_player.opponent()
            self.set_current_player(next_player)
            
            return True
        
        # Regular move if no special moves apply
        if not castle_results and not en_passant_results and not promotion_results:
            execute_move(self.engine, piece_type, player, 
                        from_pos.row, from_pos.column, to_pos.row, to_pos.column)
            
            # If this was a pawn and it made a double move, record the skipped position for en passant
            if piece_type == PieceType.PAWN:
                row_diff = abs(to_pos.row - from_pos.row)
                if row_diff == 2:
                    # Record the skipped position
                    skipped_row = (from_pos.row + to_pos.row) // 2
                    skipped_col = from_pos.column
                    self.engine.assert_fact(ChessPredicates.PAWN_SKIP, player, skipped_row, skipped_col)
            
            # Clear any existing pawn skip positions for the moving player
            var_row = self.engine.variable("Row")
            var_col = self.engine.variable("Col")
            skip_results = self.engine.query(
                ChessPredicates.PAWN_SKIP, player, var_row, var_col
            )
            
            for binding in skip_results:
                row = binding.get("Row")
                col = binding.get("Col")
                # Skip removing the one we just added
                if not (piece_type == PieceType.PAWN and abs(to_pos.row - from_pos.row) == 2 and 
                    row == (from_pos.row + to_pos.row) // 2 and col == from_pos.column):
                    self.engine.retract_fact(ChessPredicates.PAWN_SKIP, player, row, col)
            
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

    def setup_check_detection(self):
        """Setup rules for detecting check and square attacks."""
        from src.logic_engine.square_attacked import setup_square_attacked_predicate
        
        # Setup square attacked predicate
        setup_square_attacked_predicate(self.engine)
        
        var_player = self.engine.variable("Player")
        var_king_row = self.engine.variable("KingRow")
        var_king_col = self.engine.variable("KingCol")
        var_opponent = self.engine.variable("Opponent")
        
        # Player is in check if opponent can attack their king's square
        head = (ChessPredicates.IN_CHECK, 
                (var_player))
        
        body = [
            # Get the opponent player
            ("opponent", (var_player, var_opponent)),
            
            # Find the player's king
            (ChessPredicates.PIECE_AT, 
             (PieceType.KING, var_player, var_king_row, var_king_col)),
            
            # Check if king's square is attacked
            (ChessPredicates.SQUARE_ATTACKED, 
             (var_opponent, var_king_row, var_king_col))
        ]
        
        self.engine.add_rule(head, body)

    def setup_rules(self):
        """Set up the rules for the chess game."""
        from src.logic_engine.movement_rules import setup_movement_rules
        from src.logic_engine.special_moves import setup_special_moves
        
        # Setup basic movement rules
        setup_movement_rules(self.engine)
        
        # Setup special move rules (castling, en passant, promotion)
        setup_special_moves(self.engine)
        
        # Setup check and checkmate detection
        self.setup_check_detection()
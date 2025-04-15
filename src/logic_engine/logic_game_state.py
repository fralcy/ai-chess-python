"""
Logic representation of the game state.
Combines board state with game rules and state tracking.
"""

from src.logic_engine.piece_type import PieceType
from src.logic_engine.player import Player
from src.logic_engine.position import Position
from src.logic_engine.result import Result
from src.logic_engine.end_reason import EndReason
from src.logic_engine.logic_board import LogicBoard
from src.logic_engine.predicates import ChessPredicates


class LogicGameState:
    """
    Represents the state of a chess game using logic programming.
    """
    
    def __init__(self, board=None, current_player=Player.WHITE, engine=None):
        """
        Initialize the game state.
        
        Args:
            board: A Board object or None to create a new board
            current_player: The player who goes first
            engine: An existing LogicEngine instance, or None to create a new one
        """
        self.logic_board = LogicBoard(engine)
        self._result = None
        self._no_capture_or_pawn_move = 0
        self._state_history = {}
        self._position_counts = {}
        
        if board:
            # Sync from an existing board
            self.logic_board.sync_from_board(board)
        else:
            # Create a new board with initial position
            self.logic_board.setup_initial_board()
        
        # Set current player
        self.logic_board.set_current_player(current_player)
    
    @property
    def current_player(self):
        """Get the current player."""
        return self.logic_board.get_current_player()
    
    @property
    def result(self):
        """Get the game result."""
        return self._result
    
    @result.setter
    def result(self, result):
        """Set the game result."""
        self._result = result
    
    def is_in_check(self, player):
        """
        Check if a player is in check.
        
        Args:
            player: The player to check
            
        Returns:
            True if the player is in check, False otherwise
        """
        # This is a placeholder until we implement check detection rules
        # Will be properly implemented in a future commit
        return False
    
    def is_game_over(self):
        """
        Check if the game is over.
        
        Returns:
            True if the game is over, False otherwise
        """
        return self._result is not None
    
    def get_legal_moves_for(self, position):
        """
        Get all legal moves for a piece at a position.
        
        Args:
            position: The position of the piece
            
        Returns:
            A list of legal moves
        """
        # This is a placeholder until we implement move generation rules
        # Will be properly implemented in a future commit
        return []
    
    def get_all_pieces(self):
        """
        Get all pieces on the board.
        
        Returns:
            A list of tuples (piece_type, player, position, has_moved)
        """
        var_type = self.logic_board.engine.variable("Type")
        var_player = self.logic_board.engine.variable("Player")
        var_row = self.logic_board.engine.variable("Row")
        var_col = self.logic_board.engine.variable("Col")
        
        pieces = []
        results = self.logic_board.engine.query(
            ChessPredicates.PIECE_AT,
            var_type, var_player, var_row, var_col
        )
        
        for binding in results:
            piece_type = binding.get("Type")
            player = binding.get("Player")
            row = binding.get("Row")
            col = binding.get("Col")
            position = Position(row, col)
            
            # Get has_moved status
            var_moved = self.logic_board.engine.variable("Moved")
            moved_results = self.logic_board.engine.query(
                ChessPredicates.HAS_MOVED,
                piece_type, player, row, col, var_moved
            )
            
            has_moved = False
            if moved_results:
                has_moved = moved_results[0].get("Moved")
            
            pieces.append((piece_type, player, position, has_moved))
        
        return pieces
    
    def make_move(self, from_pos, to_pos):
        """
        Make a move on the board.
        
        Args:
            from_pos: The starting position
            to_pos: The destination position
            
        Returns:
            True if the move was successful, False otherwise
        """
        # Check if the game is already over
        if self.is_game_over():
            return False
        
        # Get the piece at the starting position
        piece = self.logic_board.get_piece_at(from_pos)
        if not piece:
            return False
        
        piece_type, player = piece
        
        # Check if it's the correct player's turn
        if player != self.current_player:
            return False
        
        # Execute the move
        result = self.logic_board.move_piece(from_pos, to_pos)
        
        # Update the state tracking (fifty-move rule, position counts, etc.)
        if result:
            # Check if this was a capture or pawn move
            capture_or_pawn = (piece_type == PieceType.PAWN or 
                              self.logic_board.get_piece_at(to_pos) is not None)
            
            if capture_or_pawn:
                self._no_capture_or_pawn_move = 0
            else:
                self._no_capture_or_pawn_move += 1
            
            # Update state string and position counts
            self._update_state()
            
            # Check for game over conditions
            self._check_game_over()
        
        return result
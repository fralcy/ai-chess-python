"""
Logic representation of the game state.
Combines board state with game rules and state tracking.
"""

from src.logic.player import Player
from src.logic.result import Result
from src.logic.end_reason import EndReason
from src.logic_engine.logic_board import LogicBoard
from src.logic_engine.board_adapter import BoardAdapter
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
        self.board_adapter = BoardAdapter(self.logic_board.engine)
        self._result = None
        self._no_capture_or_pawn_move = 0
        self._state_history = {}
        
        if board:
            # Sync from an existing board
            self.board_adapter.convert_to_logic(board)
        else:
            # Create a new board with initial position
            self.logic_board.setup_initial_board()
        
        # Set current player
        self.logic_board.set_current_player(current_player)
        
        # Setup rules for the chess game
        self.logic_board.setup_rules()
        
        # Initialize state string and history
        self._update_state_string()
    
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
    
    @property
    def no_capture_or_pawn_move(self):
        """Get the number of moves without capture or pawn move."""
        return self._no_capture_or_pawn_move
    
    def to_traditional_board(self):
        """
        Convert to a traditional Board object.
        
        Returns:
            A Board object representing the current state
        """
        return self.board_adapter.convert_to_traditional()
    
    def legal_moves_for_piece(self, pos):
        """
        Get all legal moves for a piece at the given position.
        To be implemented in Commit 3.
        
        Args:
            pos: The position of the piece
            
        Returns:
            A list of legal moves
        """
        # This will be implemented using logic programming in Commit 3
        # For now, return an empty list
        return []
    
    def make_move(self, move):
        """
        Make a move on the board.
        
        Args:
            move: The move to make
        """
        # Convert to traditional board to execute the move
        board = self.to_traditional_board()
        
        # Execute the move on the traditional board
        capture_or_pawn = move.execute(board)
        if capture_or_pawn:
            self._no_capture_or_pawn_move = 0
            self._state_history.clear()
        else:
            self._no_capture_or_pawn_move += 1
        
        # Convert back to logic representation
        self.board_adapter.convert_to_logic(board)
        
        # Update state string and history
        self._update_state_string()
        
        # Check for game over
        self.check_for_game_over()
    
    def _update_state_string(self):
        """Update the state string and history."""
        # Convert to traditional board to get the state string
        board = self.to_traditional_board()
        
        from src.logic.state_string import StateString
        self._state_string = str(StateString(self.current_player, board))
        
        if self._state_string in self._state_history:
            self._state_history[self._state_string] += 1
        else:
            self._state_history[self._state_string] = 1
    
    def all_legal_moves_for(self, player):
        """
        Get all legal moves for a player.
        
        Args:
            player: The player to get moves for
            
        Returns:
            A list of legal moves
        """
        # Use variables to find all piece positions
        var_piece_type = self.logic_board.engine.variable("PieceType")
        var_from_row = self.logic_board.engine.variable("FromRow")
        var_from_col = self.logic_board.engine.variable("FromCol")
        var_to_row = self.logic_board.engine.variable("ToRow")
        var_to_col = self.logic_board.engine.variable("ToCol")
        
        # Find all pieces of the player
        piece_positions = self.logic_board.engine.query(
            ChessPredicates.PIECE_AT,
            var_piece_type, player, var_from_row, var_from_col
        )
        
        all_moves = []
        
        # For each piece position, find all legal moves
        for binding in piece_positions:
            piece_type = binding.get("PieceType")
            from_row = binding.get("FromRow")
            from_col = binding.get("FromCol")
            
            # Find all legal moves for this piece
            moves = self.logic_board.engine.query(
                ChessPredicates.CAN_MOVE,
                piece_type, player, from_row, from_col, var_to_row, var_to_col
            )
            
            for move_binding in moves:
                to_row = move_binding.get("ToRow")
                to_col = move_binding.get("ToCol")
                
                # Check if the move would leave the king in check
                check_results = self.logic_board.engine.query(
                    ChessPredicates.LEAVES_IN_CHECK,
                    player, piece_type, from_row, from_col, to_row, to_col
                )
                
                # Only add the move if it doesn't leave the king in check
                if not check_results:
                    # Convert to a Move object - will need to determine the type of move
                    from src.logic.position import Position
                    from src.logic.moves.normal_move import NormalMove
                    from_pos = Position(from_row, from_col)
                    to_pos = Position(to_row, to_col)
                    all_moves.append(NormalMove(from_pos, to_pos))
        
        return all_moves
    
    def is_in_check(self, player):
        """
        Check if a player is in check.
        
        Args:
            player: The player to check
            
        Returns:
            True if the player is in check, False otherwise
        """
        results = self.logic_board.engine.query(
            ChessPredicates.IN_CHECK,
            player
        )
        
        return len(results) > 0
    
    def is_game_over(self):
        """
        Check if the game is over.
        
        Returns:
            True if the game is over, False otherwise
        """
        return self._result is not None
    
    def check_for_game_over(self):
        """Check for game over conditions and update the result if needed."""
        # Check for checkmate
        checkmate_results = self.logic_board.engine.query(
            ChessPredicates.CHECKMATE,
            self.current_player
        )
        
        if checkmate_results:
            # Game over by checkmate - opponent wins
            self._result = Result.win(self.current_player.opponent())
            return
        
        # Check for stalemate
        stalemate_results = self.logic_board.engine.query(
            ChessPredicates.STALEMATE,
            self.current_player
        )
        
        if stalemate_results:
            # Game over by stalemate - draw
            self._result = Result.draw(EndReason.STALEMATE)
            return
        
        # Check for insufficient material
        if self.logic_board.insufficient_material():
            self._result = Result.draw(EndReason.INSUFFICIENT_MATERIAL)
            return
        
        # Check for fifty-move rule
        if self.fifty_moves_rule():
            self._result = Result.draw(EndReason.FIFTY_MOVE_RULE)
            return
        
        # Check for threefold repetition
        if self.threefold_repetition():
            self._result = Result.draw(EndReason.THREEFOLD_REPETITION)
            return
    
    def fifty_moves_rule(self):
        """
        Check if the fifty-move rule applies.
        
        Returns:
            True if the fifty-move rule applies, False otherwise
        """
        full_moves = self._no_capture_or_pawn_move // 2
        return full_moves == 50
    
    def threefold_repetition(self):
        """
        Check if the threefold repetition rule applies.
        
        Returns:
            True if the threefold repetition rule applies, False otherwise
        """
        return self._state_history[self._state_string] == 3
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
            board: Không còn được sử dụng, giữ lại để tương thích
            current_player: The player who goes first
            engine: An existing LogicEngine instance, or None to create a new one
        """
        self.logic_board = LogicBoard(engine)
        self._result = None
        self._no_capture_or_pawn_move = 0
        self._state_history = {}
        self._position_counts = {}
        
        # Luôn khởi tạo bàn cờ mới
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
        return self.logic_board.is_in_check(player)
    
    def _check_game_over(self):
        """Check for game over conditions and update the result if needed."""
        # Check for checkmate
        if self.is_in_check(self.current_player) and self._has_no_legal_moves(self.current_player):
            self._result = Result.win(self.current_player.opponent())
            return True
        
        # Check for stalemate
        if not self.is_in_check(self.current_player) and self._has_no_legal_moves(self.current_player):
            self._result = Result.draw(EndReason.STALEMATE)
            return True
        
        # Check for insufficient material
        if self.logic_board.has_insufficient_material():
            self._result = Result.draw(EndReason.INSUFFICIENT_MATERIAL)
            return True
        
        # Check for fifty-move rule
        if self._no_capture_or_pawn_move >= 100:  # 50 full moves = 100 half-moves
            self._result = Result.draw(EndReason.FIFTY_MOVE_RULE)
            return True
        
        # Check for threefold repetition
        if self._position_string in self._position_counts and self._position_counts[self._position_string] >= 3:
            self._result = Result.draw(EndReason.THREEFOLD_REPETITION)
            return True
            
        return False
    
    def _has_no_legal_moves(self, player):
        """
        Check if a player has no legal moves.
        
        Args:
            player: The player to check
            
        Returns:
            True if the player has no legal moves, False otherwise
        """
        return self.logic_board.engine.query(ChessPredicates.NO_LEGAL_MOVES, player)
    
    def all_legal_moves_for(self, player):
        """
        Get all legal moves for a player.
        
        Args:
            player: The player to get moves for
            
        Returns:
            A list of legal moves
        """
        var_piece_type = self.logic_board.engine.variable("PieceType")
        var_from_row = self.logic_board.engine.variable("FromRow")
        var_from_col = self.logic_board.engine.variable("FromCol")
        var_to_row = self.logic_board.engine.variable("ToRow")
        var_to_col = self.logic_board.engine.variable("ToCol")
        
        # Query all legal moves
        results = self.logic_board.engine.query(
            ChessPredicates.CAN_MOVE,
            var_piece_type, player, var_from_row, var_from_col, var_to_row, var_to_col
        )
        
        # Filter out moves that would leave the king in check
        legal_moves = []
        from src.logic_engine.move import Move
        from src.logic_engine.position import Position
        
        for binding in results:
            piece_type = binding.get("PieceType")
            from_row = binding.get("FromRow")
            from_col = binding.get("FromCol")
            to_row = binding.get("ToRow")
            to_col = binding.get("ToCol")
            
            # Check if the move would leave the king in check
            check_results = self.logic_board.engine.query(
                ChessPredicates.LEAVES_IN_CHECK,
                player, piece_type, from_row, from_col, to_row, to_col
            )
            
            if not check_results:
                # Create a Move object for this legal move
                from_pos = Position(from_row, from_col)
                to_pos = Position(to_row, to_col)
                
                # Determine move type
                from src.logic_engine.move_type import MoveType
                move_type = MoveType.NORMAL  # Default move type
                
                # Check for special move types
                if piece_type == PieceType.KING and abs(from_col - to_col) == 2:
                    # Castling
                    move_type = MoveType.CASTLE_KS if to_col > from_col else MoveType.CASTLE_QS
                elif piece_type == PieceType.PAWN:
                    # Check for pawn promotion
                    if (player == Player.WHITE and to_row == 0) or (player == Player.BLACK and to_row == 7):
                        move_type = MoveType.PAWN_PROMOTION
                    # Check for double pawn move
                    elif abs(from_row - to_row) == 2:
                        move_type = MoveType.DOUBLE_PAWN
                    # Check for en passant
                    elif from_col != to_col and self.logic_board.is_square_empty(to_pos):
                        move_type = MoveType.EN_PASSANT
                
                # Create the move
                legal_moves.append(Move(from_pos, to_pos, move_type))
        
        return legal_moves
    
    def legal_moves_for_piece(self, position):
        """
        Get all legal moves for a piece at a position.
        
        Args:
            position: The position of the piece
            
        Returns:
            A list of legal moves
        """
        piece = self.logic_board.get_piece_at(position)
        if not piece:
            return []
        
        piece_type, player = piece
        
        # If it's not this player's turn, no legal moves
        if player != self.current_player:
            return []
        
        var_to_row = self.logic_board.engine.variable("ToRow")
        var_to_col = self.logic_board.engine.variable("ToCol")
        
        # Query all possible moves for this piece
        results = self.logic_board.engine.query(
            ChessPredicates.CAN_MOVE,
            piece_type, player, position.row, position.column, var_to_row, var_to_col
        )
        
        # Filter out moves that would leave the king in check
        legal_moves = []
        from src.logic_engine.move import Move
        
        for binding in results:
            to_row = binding.get("ToRow")
            to_col = binding.get("ToCol")
            
            # Check if the move would leave the king in check
            check_results = self.logic_board.engine.query(
                ChessPredicates.LEAVES_IN_CHECK,
                player, piece_type, position.row, position.column, to_row, to_col
            )
            
            if not check_results:
                # Create a Move object for this legal move
                from src.logic_engine.position import Position
                to_pos = Position(to_row, to_col)
                
                # Determine move type
                from src.logic_engine.move_type import MoveType
                move_type = MoveType.NORMAL  # Default move type
                
                # Check for special move types
                if piece_type == PieceType.KING and abs(position.column - to_col) == 2:
                    # Castling
                    move_type = MoveType.CASTLE_KS if to_col > position.column else MoveType.CASTLE_QS
                elif piece_type == PieceType.PAWN:
                    # Check for pawn promotion
                    if (player == Player.WHITE and to_row == 0) or (player == Player.BLACK and to_row == 7):
                        move_type = MoveType.PAWN_PROMOTION
                    # Check for double pawn move
                    elif abs(position.row - to_row) == 2:
                        move_type = MoveType.DOUBLE_PAWN
                    # Check for en passant
                    elif position.column != to_col and self.logic_board.is_square_empty(to_pos):
                        move_type = MoveType.EN_PASSANT
                
                # Create the move
                legal_moves.append(Move(position, to_pos, move_type))
        
        return legal_moves
    
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
    
    def make_move(self, move):
        """
        Make a move on the board.
        
        Args:
            move: A Move object
            
        Returns:
            True if the move was successful, False otherwise
        """
        # Check if the game is already over
        if self.is_game_over():
            return False
        
        from_pos = move.from_pos
        to_pos = move.to_pos
        
        # Get the piece at the starting position
        piece = self.logic_board.get_piece_at(from_pos)
        if not piece:
            return False
        
        piece_type, player = piece
        
        # Check if it's the correct player's turn
        if player != self.current_player:
            return False
        
        # Check if the move is legal
        move_type = move.type
        if not self._is_legal_move(from_pos, to_pos, move_type):
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
            
            # Update position string and position counts
            self._update_state()
            
            # Check for game over conditions
            self._check_game_over()
        
        return result
    
    def _is_legal_move(self, from_pos, to_pos, move_type):
        """
        Check if a move is legal.
        
        Args:
            from_pos: The starting position
            to_pos: The destination position
            move_type: The type of move
            
        Returns:
            True if the move is legal, False otherwise
        """
        piece = self.logic_board.get_piece_at(from_pos)
        if not piece:
            return False
        
        piece_type, player = piece
        
        # Check if the move is valid according to chess rules
        var_type = self.logic_board.engine.variable("Type")
        results = self.logic_board.engine.query(
            ChessPredicates.CAN_MOVE,
            piece_type, player, from_pos.row, from_pos.column, to_pos.row, to_pos.column
        )
        
        if not results:
            return False
        
        # Check if the move would leave the king in check
        check_results = self.logic_board.engine.query(
            ChessPredicates.LEAVES_IN_CHECK,
            player, piece_type, from_pos.row, from_pos.column, to_pos.row, to_pos.column
        )
        
        return len(check_results) == 0
    
    def is_game_over(self):
        """
        Check if the game is over.
        
        Returns:
            True if the game is over, False otherwise
        """
        return self._result is not None
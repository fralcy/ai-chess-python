from logic.pieces.piece import Piece
from logic.player import Player
from logic.result import Result
from logic.end_reason import EndReason

class GameState:
    def __init__(self, board, current_player):
        self._board = board
        self._current_player = current_player
        self._result = None
    
    @property
    def board(self):
        return self._board
    
    @property
    def current_player(self):
        return self._current_player
    
    @current_player.setter
    def current_player(self, player):
        self._current_player = player

    @property
    def result(self):
        return self._result
    
    @result.setter
    def result(self, result):
        self._result = result
    
    def copy(self):
        """Create a deep copy of the game state for move simulation."""
        board_copy = self._board.copy()
        new_state = GameState(board_copy, self._current_player)
        if self._result:
            new_state._result = self._result  # Copy the result if game is over
        return new_state

    def legal_moves_for_piece(self, pos):
        """Get all legal moves for a piece at the given position."""
        piece = self._board.get_piece(pos)
        if piece is None or piece.color != self._current_player:
            return []

        # Get all possible moves
        all_moves = list(piece.get_moves(pos, self._board))
        
        # Filter out moves that would leave the player in check
        legal_moves = []
        for move in all_moves:
            if move.is_legal(self._board):
                legal_moves.append(move)
                
        return legal_moves
    
    def make_move(self, move):
        """Execute a move and update the game state."""
        self._board.set_pawn_skip_position(self._current_player, None)
        move.execute(self._board)
        self._current_player = self._current_player.opponent()
        self.check_for_game_over()

    def all_legal_moves_for(self, player):
        """Get all legal moves for a player."""
        all_moves = []
        for pos in self._board.piece_positions_for(player):
            all_moves.extend(self.legal_moves_for_piece(pos))
        return all_moves
    
    def is_in_check(self, player):
        """Check if a player is in check."""
        return self._board.is_in_check(player)
    
    def check_for_game_over(self):
        """Check if the game is over and update the result."""
        if len(self.all_legal_moves_for(self._current_player)) == 0:
            if self._board.is_in_check(self._current_player):
                self._result = Result(self._current_player.opponent(), EndReason.CHECKMATE)
            else:
                self._result = Result(Player.NONE, EndReason.STALEMATE)

    def is_game_over(self):
        """Check if the game is over."""
        return self._result is not None
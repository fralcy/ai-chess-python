from logic.pieces.piece import Piece
from logic.player import Player
from logic.result import Result
from logic.end_reason import EndReason
class GameState():
    def __init__(self, board, current_player):
        self._board = board
        self._current_player = current_player
        self._result = None
        self._no_capture_or_pawn_move = 0
    
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
    def result(self) -> Result:
        return self._result
    
    @result.setter
    def result(self, result):
        self._result = result

    @property
    def no_capture_or_pawn_move(self) -> int:
        return self._no_capture_or_pawn_move

    def legal_moves_for_piece(self, pos):
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
        self._board.set_pawn_skip_position(self._current_player, None)
        capture_or_pawn = move.execute(self._board)
        if capture_or_pawn:
            self._no_capture_or_pawn_move = 0
        else:
            self._no_capture_or_pawn_move += 1
        self._current_player = self._current_player.opponent()
        self.check_for_game_over()

    def all_legal_moves_for(self, player):
        all_moves = []
        for pos in self._board.piece_positions_for(player):
            all_moves.extend(self.legal_moves_for_piece(pos))
        return all_moves
    
    def check_for_game_over(self):
        if len(self.all_legal_moves_for(self._current_player)) == 0:
            if self._board.is_in_check(self._current_player):
                self._result = Result.win(self._current_player.opponent())
            else:
                self._result = Result.draw(EndReason.STALEMATE)
        elif self._board.insufficient_material():
            self._result = Result.draw(EndReason.INSUFFICIENT_MATERIAL);
        elif self.fifty_moves_rule():
            self._result = Result.draw(EndReason.FIFTY_MOVE_RULE);

    def is_game_over(self):
        return self._result is not None
    
    def fifty_moves_rule(self) -> bool:
        full_moves = self._no_capture_or_pawn_move // 2
        return full_moves == 50
from logic.pieces.piece import Piece

class GameState():
    def __init__(self, board, current_player):
        self._board = board
        self._current_player = current_player
    
    @property
    def board(self):
        return self._board
    
    @property
    def current_player(self):
        return self._current_player
    
    @current_player.setter
    def current_player(self, player):
        self._current_player = player
    
    def legal_moves_for_piece(self, pos):
        if self._board[pos].is_empty() or self._board[pos].player != self._current_player:
            return []
        
        piece = self._board[pos]
        return piece.get_moves(pos, self._board)
    
    def make_move(self, move):
        move.execute(self._board)
        self._current_player = self._current_player.opponent()
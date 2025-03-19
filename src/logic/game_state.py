
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
    
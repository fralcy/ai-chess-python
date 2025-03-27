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
        piece = self._board.get_piece(pos)
        if piece is None or piece.color != self._current_player:
            return []

        # Get all possible moves
        all_moves = list(piece.get_moves(pos, self._board))
        
        # Filter out moves that would leave the player in check
        legal_moves = []
        for move in all_moves:
            if move.is_legal(self._board, self._current_player):
                legal_moves.append(move)
                
        return legal_moves
    
    def make_move(self, move):
        move.execute(self._board)
        self._current_player = self._current_player.opponent()
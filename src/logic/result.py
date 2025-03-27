from logic.player import Player
from logic.end_reason import EndReason

class Result:
    @property
    def winner(self):
        return self._winner
    
    @property
    def end_reason(self):
        return self._end_reason
    
    def __init__(self, winner: Player, end_reason: EndReason):
        self._winner = winner
        self._end_reason = end_reason

    def __win__(self, winner: Player):
        return Result(winner, EndReason.CHECKMATE)
    
    def __draw__(self):
        return Result(Player.NONE, EndReason.STALEMATE)
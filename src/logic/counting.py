from logic.piece_type import PieceType
from typing import Dict
from logic.player import Player

class Counting:
    @property
    def total_count(self) -> int:
        return self._total_count
    
    @total_count.setter
    def total_count(self, value: int):
        self._total_count = value

    def __init__(self):
        self._white_count: Dict[PieceType, int] = {}
        self._black_count: Dict[PieceType, int] = {}
        self._total_count = 0
        
        # Initialize counts for all piece types to zero
        for piece_type in PieceType:
            self._white_count[piece_type] = 0
            self._black_count[piece_type] = 0
    
    def increment(self, color: Player, piece_type: PieceType) -> None:
        if color == Player.WHITE:
            self._white_count[piece_type] += 1
        elif color == Player.BLACK:
            self._black_count[piece_type] += 1
        else:
            raise ValueError("Player must be either 'white' or 'black'")
        
        self._total_count += 1

    def White(self, piece_type: PieceType) -> int:
        return self._white_count[piece_type]
    
    def Black(self, piece_type: PieceType) -> int:
        return self._black_count[piece_type]
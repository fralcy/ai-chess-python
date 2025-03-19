# Import all piece classes to make them available from the pieces package
from src.logic.pieces.pawn import Pawn
from src.logic.pieces.knight import Knight
from src.logic.pieces.bishop import Bishop
from src.logic.pieces.rook import Rook
from src.logic.pieces.queen import Queen
from src.logic.pieces.king import King

# Export all classes to make them directly importable from pieces
__all__ = ['Pawn', 'Knight', 'Bishop', 'Rook', 'Queen', 'King']
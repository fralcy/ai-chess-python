"""
Constants for the chess game
"""
import os

# Window settings
WIDTH = 800
HEIGHT = 800
TITLE = "Chess Game with AI"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT = (247, 247, 105, 150)  # Highlight color for selected piece
MOVE_HIGHLIGHT = (106, 168, 79, 150)  # Highlight color for possible moves

# Board settings
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE

# Game settings
FPS = 60

# Assets paths
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
PIECES_DIR = os.path.join(ASSETS_DIR, 'images')

# Mapping piece codes to image filenames
PIECE_IMAGES = {
    ('K', 'white'): os.path.join(PIECES_DIR, 'white_king.png'),
    ('Q', 'white'): os.path.join(PIECES_DIR, 'white_queen.png'),
    ('R', 'white'): os.path.join(PIECES_DIR, 'white_rook.png'),
    ('B', 'white'): os.path.join(PIECES_DIR, 'white_bishop.png'),
    ('N', 'white'): os.path.join(PIECES_DIR, 'white_knight.png'),
    ('P', 'white'): os.path.join(PIECES_DIR, 'white_pawn.png'),
    ('K', 'black'): os.path.join(PIECES_DIR, 'black_king.png'),
    ('Q', 'black'): os.path.join(PIECES_DIR, 'black_queen.png'),
    ('R', 'black'): os.path.join(PIECES_DIR, 'black_rook.png'),
    ('B', 'black'): os.path.join(PIECES_DIR, 'black_bishop.png'),
    ('N', 'black'): os.path.join(PIECES_DIR, 'black_knight.png'),
    ('P', 'black'): os.path.join(PIECES_DIR, 'black_pawn.png'),
}
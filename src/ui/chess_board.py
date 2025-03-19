import pygame
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.board import Board
from logic.player import Player
from logic.piece_type import PieceType

class ChessBoard:
    # Colors
    LIGHT_SQUARE = (240, 217, 181)  # Beige color for light squares
    DARK_SQUARE = (181, 136, 99)    # Brown color for dark squares
    
    # Board dimensions
    SQUARE_SIZE = 80
    BOARD_SIZE = SQUARE_SIZE * 8
    
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.load_pieces_images()
        
    def load_pieces_images(self):
        """Load chess piece images."""
        self.piece_images = {}
        pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        colors = ['white', 'black']
        
        for piece in pieces:
            for color in colors:
                image_path = f'assets/images/{color}_{piece}.png'
                try:
                    # Load and scale the image to fit squares
                    img = pygame.image.load(image_path)
                    img = pygame.transform.scale(img, (self.SQUARE_SIZE, self.SQUARE_SIZE))
                    
                    # Create key for the image dictionary
                    piece_type = getattr(PieceType, piece.upper())
                    player = Player.WHITE if color == 'white' else Player.BLACK
                    self.piece_images[(player, piece_type)] = img
                except pygame.error as e:
                    print(f"Cannot load image: {image_path}")
                    print(f"Error: {e}")
    
    def draw_board(self):
        """Draw the chess board with alternating colors."""
        # Create font for labels
        font = pygame.font.SysFont('Arial', 16)
        
        for row in range(8):
            for col in range(8):
                # Determine square color
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                
                # Draw square
                pygame.draw.rect(
                    self.screen,
                    color,
                    (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, 
                     self.SQUARE_SIZE, self.SQUARE_SIZE)
                )
                
                # Add row and column labels
                if col == 0:  # Numbers on the left edge (rows)
                    text_color = self.DARK_SQUARE if (row + col) % 2 == 0 else self.LIGHT_SQUARE
                    label = font.render(str(8 - row), True, text_color)
                    self.screen.blit(label, (5, row * self.SQUARE_SIZE + 5))
                
                if row == 7:  # Letters on the bottom edge (columns)
                    text_color = self.DARK_SQUARE if (row + col) % 2 == 0 else self.LIGHT_SQUARE
                    label = font.render(chr(97 + col), True, text_color)  # 'a' through 'h'
                    self.screen.blit(label, (col * self.SQUARE_SIZE + self.SQUARE_SIZE - 15, 
                                           self.BOARD_SIZE - 20))
    
    def draw_pieces(self):
        """Draw pieces on the board according to the current board state."""
        from ui.fallback_renderer import FallbackRenderer
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece:
                    image_key = (piece.color, piece.piece_type)
                    if image_key in self.piece_images:
                        self.screen.blit(
                            self.piece_images[image_key],
                            (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE)
                        )
                    else:
                        # Use fallback renderer if image not available
                        FallbackRenderer.render_piece(
                            self.screen, 
                            piece, 
                            col * self.SQUARE_SIZE, 
                            row * self.SQUARE_SIZE, 
                            self.SQUARE_SIZE
                        )
    
    def draw(self):
        """Draw the complete chess board with pieces."""
        self.draw_board()
        self.draw_pieces()
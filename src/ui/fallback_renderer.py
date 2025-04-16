import pygame
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.logic_engine.piece_type import PieceType
from src.logic_engine.player import Player

class FallbackRenderer:
    """Class that can render chess pieces when images are unavailable."""
    
    # Colors
    WHITE_PIECE = (255, 255, 255)  # White for white pieces
    BLACK_PIECE = (0, 0, 0)        # Black for black pieces
    
    @staticmethod
    def render_piece(screen, piece, x, y, square_size):
        """Render a piece using simple shapes when images aren't available."""
        if not piece:
            return
            
        # Determine piece color
        color = FallbackRenderer.WHITE_PIECE if piece.color == Player.WHITE else FallbackRenderer.BLACK_PIECE
        
        # Calculate center of the square
        center_x = x + square_size // 2
        center_y = y + square_size // 2
        
        # Radius for circle-based shapes
        radius = square_size // 3
        
        # Smaller radius for dots
        small_radius = square_size // 8
        
        # Draw piece based on its type
        if piece.piece_type == PieceType.PAWN:
            pygame.draw.circle(screen, color, (center_x, center_y), radius)
            
        elif piece.piece_type == PieceType.KNIGHT:
            # Knight - Circle with a small circle on top
            pygame.draw.circle(screen, color, (center_x, center_y), radius)
            pygame.draw.circle(screen, color, (center_x, center_y - radius), small_radius)
            
        elif piece.piece_type == PieceType.BISHOP:
            # Bishop - Circle with a cross on top
            pygame.draw.circle(screen, color, (center_x, center_y), radius)
            pygame.draw.line(screen, color, (center_x - radius//2, center_y - radius//2), 
                            (center_x + radius//2, center_y + radius//2), 2)
            pygame.draw.line(screen, color, (center_x + radius//2, center_y - radius//2), 
                            (center_x - radius//2, center_y + radius//2), 2)
            
        elif piece.piece_type == PieceType.ROOK:
            # Rook - Square
            square_rect = pygame.Rect(center_x - radius, center_y - radius, 
                                    radius * 2, radius * 2)
            pygame.draw.rect(screen, color, square_rect)
            
        elif piece.piece_type == PieceType.QUEEN:
            # Queen - Circle with a crown-like shape
            pygame.draw.circle(screen, color, (center_x, center_y), radius)
            
            # Draw small circles around the top (crown)
            for i in range(5):
                angle = -90 + i * 45  # -90 degrees is top, we go around in 45 degree steps
                offset_x = int(radius * 0.8 * pygame.math.Vector2(1, 0).rotate(angle).x)
                offset_y = int(radius * 0.8 * pygame.math.Vector2(1, 0).rotate(angle).y)
                pygame.draw.circle(screen, color, (center_x + offset_x, center_y + offset_y), small_radius)
            
        elif piece.piece_type == PieceType.KING:
            # King - Circle with a cross
            pygame.draw.circle(screen, color, (center_x, center_y), radius)
            
            # Vertical line
            pygame.draw.line(screen, color, (center_x, center_y - radius - small_radius), 
                           (center_x, center_y + radius + small_radius), 3)
            
            # Horizontal line
            pygame.draw.line(screen, color, (center_x - radius - small_radius, center_y), 
                           (center_x + radius + small_radius, center_y), 3)
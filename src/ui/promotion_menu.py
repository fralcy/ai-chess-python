import pygame
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.logic_engine.piece_type import PieceType
from src.logic_engine.player import Player
from ui.fallback_renderer import FallbackRenderer

class PromotionMenu:
    """A menu for selecting a piece when promoting a pawn."""
    
    # Colors
    BACKGROUND_COLOR = (0, 0, 0, 200)  # Semi-transparent black
    TEXT_COLOR = (255, 215, 0)  # Gold for text
    HOVER_COLOR = (100, 149, 237, 150)  # Semi-transparent blue for hover effect
    
    # Available promotion pieces
    PROMOTION_PIECES = [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]
    
    def __init__(self, screen, player, square_size):
        """Initialize the promotion menu.
        
        Args:
            screen: The pygame screen to draw on
            player: The player who is promoting (Player enum)
            square_size: The size of a chess square
        """
        self.screen = screen
        self.player = player
        self.square_size = square_size
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Create fonts
        try:
            self.title_font = pygame.font.Font("freesansbold.ttf", 32)
        except:
            self.title_font = pygame.font.SysFont('Arial', 32, bold=True)
            
        # Calculate positions
        menu_width = len(self.PROMOTION_PIECES) * square_size
        menu_height = square_size * 2  # Title row + pieces row
        
        self.menu_rect = pygame.Rect(
            (self.screen_width - menu_width) // 2,
            (self.screen_height - menu_height) // 2,
            menu_width,
            menu_height
        )
        
        # Setup piece buttons
        self.piece_rects = []
        for i, piece_type in enumerate(self.PROMOTION_PIECES):
            self.piece_rects.append(
                pygame.Rect(
                    self.menu_rect.left + i * square_size,
                    self.menu_rect.top + square_size,  # Below the title
                    square_size,
                    square_size
                )
            )
        
        # Try to load piece images
        self.piece_images = {}
        self.load_piece_images()
    
    def load_piece_images(self):
        """Load chess piece images."""
        color_name = 'white' if self.player == Player.WHITE else 'black'
        
        for piece_type in self.PROMOTION_PIECES:
            piece_name = piece_type.name.lower()
            image_path = f'assets/images/{color_name}_{piece_name}.png'
            
            try:
                # Load and scale the image to fit squares
                img = pygame.image.load(image_path)
                img = pygame.transform.scale(img, (self.square_size, self.square_size))
                self.piece_images[piece_type] = img
            except pygame.error as e:
                print(f"Cannot load promotion piece image: {image_path}")
                print(f"Error: {e}")
    
    def draw(self):
        """Draw the promotion menu."""
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill(self.BACKGROUND_COLOR)
        self.screen.blit(overlay, (0, 0))
        
        # Draw the menu background
        pygame.draw.rect(self.screen, (50, 50, 50), self.menu_rect, border_radius=10)
        pygame.draw.rect(self.screen, (150, 150, 150), self.menu_rect, width=2, border_radius=10)
        
        # Draw title
        title_text = self.title_font.render("Select a Piece", True, self.TEXT_COLOR)
        title_rect = title_text.get_rect(
            center=(self.menu_rect.centerx, self.menu_rect.top + self.square_size // 2)
        )
        self.screen.blit(title_text, title_rect)
        
        # Draw piece options with hover effect
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (piece_rect, piece_type) in enumerate(zip(self.piece_rects, self.PROMOTION_PIECES)):
            # Draw hover effect
            if piece_rect.collidepoint(mouse_pos):
                hover_surface = pygame.Surface((piece_rect.width, piece_rect.height), pygame.SRCALPHA)
                hover_surface.fill(self.HOVER_COLOR)
                self.screen.blit(hover_surface, piece_rect)
            
            # Draw piece image or fallback shape
            if piece_type in self.piece_images:
                self.screen.blit(self.piece_images[piece_type], piece_rect)
            else:
                # Create a temporary piece object for the fallback renderer
                class TempPiece:
                    def __init__(self, piece_type, color):
                        self.piece_type = piece_type
                        self.color = color
                
                temp_piece = TempPiece(piece_type, self.player)
                FallbackRenderer.render_piece(
                    self.screen,
                    temp_piece,
                    piece_rect.left,
                    piece_rect.top,
                    self.square_size
                )
    
    def handle_click(self, event):
        """Handle clicks on the promotion menu.
        
        Args:
            event: The pygame event
            
        Returns:
            The selected piece type or None if no selection was made
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, piece_rect in enumerate(self.piece_rects):
                if piece_rect.collidepoint(event.pos):
                    return self.PROMOTION_PIECES[i]
        
        return None
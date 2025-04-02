import pygame
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.option import Option

class PauseMenu:
    """A simple pause menu for the chess game."""
    
    # Colors
    BACKGROUND_COLOR = (0, 0, 0, 200)  # Semi-transparent black
    TEXT_COLOR = (255, 215, 0)  # Gold for text
    BUTTON_COLOR = (70, 130, 180)  # Steel blue
    BUTTON_HOVER_COLOR = (100, 149, 237)  # Cornflower blue
    BUTTON_TEXT_COLOR = (255, 255, 255)  # White
    
    def __init__(self, screen):
        """Initialize the pause menu.
        
        Args:
            screen: The pygame screen to draw on
        """
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Create fonts
        try:
            self.title_font = pygame.font.Font("freesansbold.ttf", 46)
        except:
            self.title_font = pygame.font.SysFont('Arial', 46, bold=True)
            
        try:
            self.button_font = pygame.font.Font("freesansbold.ttf", 24)
        except:
            self.button_font = pygame.font.SysFont('Arial', 24)
        
        # Create buttons
        button_width = 160
        button_height = 60
        button_y_top = self.screen_height // 2 - 40
        button_y_bottom = self.screen_height // 2 + 40
        
        self.continue_button = pygame.Rect(
            self.screen_width // 2 - button_width - 30,
            button_y_top,
            button_width,
            button_height
        )
        
        self.restart_button = pygame.Rect(
            self.screen_width // 2 + 30,
            button_y_top,
            button_width,
            button_height
        )
        
        # Thêm nút để quay về AI menu
        self.ai_menu_button = pygame.Rect(
            (self.screen_width - button_width) // 2,
            button_y_bottom,
            button_width,
            button_height
        )
    
    def draw(self):
        """Draw the pause menu."""
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill(self.BACKGROUND_COLOR)
        self.screen.blit(overlay, (0, 0))
        
        # Draw a decorative panel in the center
        panel_width = self.screen_width * 0.7
        panel_height = self.screen_height * 0.5  # Tăng chiều cao để chứa nút mới
        panel_rect = pygame.Rect(
            (self.screen_width - panel_width) // 2,
            (self.screen_height - panel_height) // 2,
            panel_width,
            panel_height
        )
        pygame.draw.rect(self.screen, (30, 30, 30, 220), panel_rect, border_radius=15)
        
        # Add a border to the panel
        pygame.draw.rect(self.screen, (100, 100, 100, 150), panel_rect, width=2, border_radius=15)
        
        # Draw title text
        title_surface = self.title_font.render("Game Paused", True, self.TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
        self.screen.blit(title_surface, title_rect)
        
        # Draw buttons with improved appearance
        mouse_pos = pygame.mouse.get_pos()
        
        # Continue button (with hover effect and shadow)
        continue_color = self.BUTTON_HOVER_COLOR if self.continue_button.collidepoint(mouse_pos) else self.BUTTON_COLOR
        
        # Button shadow
        shadow_rect = self.continue_button.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (20, 20, 20), shadow_rect, border_radius=10)
        
        # Main button
        pygame.draw.rect(self.screen, continue_color, self.continue_button, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255, 100), self.continue_button, width=2, border_radius=10)
        continue_text = self.button_font.render("Continue", True, self.BUTTON_TEXT_COLOR)
        continue_text_rect = continue_text.get_rect(center=self.continue_button.center)
        self.screen.blit(continue_text, continue_text_rect)
        
        # Restart button (with hover effect and shadow)
        restart_color = self.BUTTON_HOVER_COLOR if self.restart_button.collidepoint(mouse_pos) else self.BUTTON_COLOR
        
        # Button shadow
        shadow_rect = self.restart_button.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (20, 20, 20), shadow_rect, border_radius=10)
        
        # Main button
        pygame.draw.rect(self.screen, restart_color, self.restart_button, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255, 100), self.restart_button, width=2, border_radius=10)
        restart_text = self.button_font.render("Restart", True, self.BUTTON_TEXT_COLOR)
        restart_text_rect = restart_text.get_rect(center=self.restart_button.center)
        self.screen.blit(restart_text, restart_text_rect)
        
        # AI Menu button (with hover effect and shadow)
        ai_menu_color = self.BUTTON_HOVER_COLOR if self.ai_menu_button.collidepoint(mouse_pos) else self.BUTTON_COLOR
        
        # Button shadow
        shadow_rect = self.ai_menu_button.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (20, 20, 20), shadow_rect, border_radius=10)
        
        # Main button
        pygame.draw.rect(self.screen, ai_menu_color, self.ai_menu_button, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255, 100), self.ai_menu_button, width=2, border_radius=10)
        ai_menu_text = self.button_font.render("AI Menu", True, self.BUTTON_TEXT_COLOR)
        ai_menu_text_rect = ai_menu_text.get_rect(center=self.ai_menu_button.center)
        self.screen.blit(ai_menu_text, ai_menu_text_rect)
    
    def handle_event(self, event):
        """Handle mouse clicks and keyboard events.
        
        Args:
            event: The pygame event
            
        Returns:
            Option indicating which button was clicked, or None if no button was clicked
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.continue_button.collidepoint(event.pos):
                return Option.CONTINUE
            elif self.restart_button.collidepoint(event.pos):
                return Option.RESTART
            elif self.ai_menu_button.collidepoint(event.pos):
                return Option.EXIT  # Sử dụng EXIT để quay về AI menu
        
        # Also handle Escape key to continue the game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return Option.CONTINUE
            
        return None
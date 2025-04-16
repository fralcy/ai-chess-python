import pygame
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class AIMenu:
    """A menu for selecting AI options."""
    
    # Colors
    BACKGROUND_COLOR = (0, 0, 0, 200)  # Semi-transparent black
    TEXT_COLOR = (255, 215, 0)  # Gold for text
    BUTTON_COLOR = (70, 130, 180)  # Steel blue
    BUTTON_HOVER_COLOR = (100, 149, 237)  # Cornflower blue
    BUTTON_TEXT_COLOR = (255, 255, 255)  # White
    SELECTED_COLOR = (50, 205, 50)  # Lime green for selected button
    
    def __init__(self, screen):
        """Initialize the AI menu.
        
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
            self.subtitle_font = pygame.font.Font("freesansbold.ttf", 32)
        except:
            self.subtitle_font = pygame.font.SysFont('Arial', 32)
            
        try:
            self.button_font = pygame.font.Font("freesansbold.ttf", 24)
        except:
            self.button_font = pygame.font.SysFont('Arial', 24)
        
        # Tạo panel chính
        panel_width = self.screen_width * 0.8
        panel_height = self.screen_height * 0.7
        self.panel_rect = pygame.Rect(
            (self.screen_width - panel_width) // 2,
            (self.screen_height - panel_height) // 2,
            panel_width,
            panel_height
        )
        
        # Giảm khoảng cách từ tiêu đề xuống phần "Play as"
        title_y = self.panel_rect.top + 40  # Giảm từ 50 xuống 40
        
        # Tính toán vị trí cho phần Play as
        play_as_y = title_y + 70  # Giảm khoảng cách giữa tiêu đề và "Play as"
        
        # Create play mode buttons
        button_width = 180
        button_height = 60
        button_spacing = 40  # Khoảng cách giữa các nút màu
        
        # Tính toán vị trí cho các nút màu sắc
        color_buttons_y = play_as_y + 50
        
        self.play_as_white_button = pygame.Rect(
            self.screen_width // 2 - button_width - button_spacing // 2,
            color_buttons_y,
            button_width,
            button_height
        )
        
        self.play_as_black_button = pygame.Rect(
            self.screen_width // 2 + button_spacing // 2,
            color_buttons_y,
            button_width,
            button_height
        )
        
        # Tính toán vị trí cho phần Difficulty
        diff_y = color_buttons_y + button_height + 30  # Giảm khoảng cách giữa các nút màu và "Difficulty"
        
        # Create difficulty buttons
        diff_button_width = 70
        diff_button_height = 50
        diff_button_spacing = 10  # Khoảng cách giữa các nút khó
        
        # Tính tổng chiều rộng của các nút khó + khoảng cách
        total_diff_width = 5 * diff_button_width + 4 * diff_button_spacing
        
        # Tính vị trí bắt đầu để căn giữa các nút khó
        diff_start_x = (self.screen_width - total_diff_width) // 2
        
        # Tính toán vị trí cho các nút độ khó
        diff_buttons_y = diff_y + 50
        
        self.difficulty_buttons = []
        for i in range(5):
            button = pygame.Rect(
                diff_start_x + i * (diff_button_width + diff_button_spacing),
                diff_buttons_y,
                diff_button_width,
                diff_button_height
            )
            self.difficulty_buttons.append(button)
        
        # Default selections
        self.player_color = "white"  # Default: player is white
        self.difficulty = 3  # Default: medium difficulty (1-5)
        
        # Tính toán vị trí cho nút Start game
        start_button_y = diff_buttons_y + diff_button_height + 40  # Giảm khoảng cách xuống nút Start
        
        # Start button
        self.start_button = pygame.Rect(
            (self.screen_width - 200) // 2,
            start_button_y,
            200,
            70
        )
    
    def draw(self):
        """Draw the AI menu."""
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill(self.BACKGROUND_COLOR)
        self.screen.blit(overlay, (0, 0))
        
        # Draw a decorative panel in the center
        pygame.draw.rect(self.screen, (30, 30, 30, 220), self.panel_rect, border_radius=15)
        
        # Add a border to the panel
        pygame.draw.rect(self.screen, (100, 100, 100, 150), self.panel_rect, width=2, border_radius=15)
        
        # Draw title
        title_surface = self.title_font.render("Game Options", True, self.TEXT_COLOR)
        title_rect = title_surface.get_rect(
            center=(self.screen_width // 2, self.panel_rect.top + 40)  # Giảm từ 50 xuống 40
        )
        self.screen.blit(title_surface, title_rect)
        
        # Draw subtitle for player color
        color_text = self.subtitle_font.render("Play as:", True, (200, 200, 200))
        self.screen.blit(color_text, (self.panel_rect.left + 50, self.play_as_white_button.top - 50))
        
        # Draw player color buttons
        mouse_pos = pygame.mouse.get_pos()
        
        # White button
        white_color = self.SELECTED_COLOR if self.player_color == "white" else (
            self.BUTTON_HOVER_COLOR if self.play_as_white_button.collidepoint(mouse_pos) else self.BUTTON_COLOR
        )
        pygame.draw.rect(self.screen, white_color, self.play_as_white_button, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255, 100), self.play_as_white_button, width=2, border_radius=10)
        white_text = self.button_font.render("White", True, self.BUTTON_TEXT_COLOR)
        white_text_rect = white_text.get_rect(center=self.play_as_white_button.center)
        self.screen.blit(white_text, white_text_rect)
        
        # Black button
        black_color = self.SELECTED_COLOR if self.player_color == "black" else (
            self.BUTTON_HOVER_COLOR if self.play_as_black_button.collidepoint(mouse_pos) else self.BUTTON_COLOR
        )
        pygame.draw.rect(self.screen, black_color, self.play_as_black_button, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255, 100), self.play_as_black_button, width=2, border_radius=10)
        black_text = self.button_font.render("Black", True, self.BUTTON_TEXT_COLOR)
        black_text_rect = black_text.get_rect(center=self.play_as_black_button.center)
        self.screen.blit(black_text, black_text_rect)
        
        # Draw subtitle for difficulty
        diff_text = self.subtitle_font.render("Difficulty:", True, (200, 200, 200))
        self.screen.blit(diff_text, (self.panel_rect.left + 50, self.difficulty_buttons[0].top - 50))
        
        # Draw difficulty buttons
        diff_labels = ["1", "2", "3", "4", "5"]
        
        for i, button in enumerate(self.difficulty_buttons):
            # Determine button color based on selection and hover state
            button_color = self.SELECTED_COLOR if self.difficulty == i + 1 else (
                self.BUTTON_HOVER_COLOR if button.collidepoint(mouse_pos) else self.BUTTON_COLOR
            )
            
            # Draw button
            pygame.draw.rect(self.screen, button_color, button, border_radius=8)
            pygame.draw.rect(self.screen, (255, 255, 255, 100), button, width=2, border_radius=8)
            
            # Draw button text
            button_text = self.button_font.render(diff_labels[i], True, self.BUTTON_TEXT_COLOR)
            button_text_rect = button_text.get_rect(center=button.center)
            self.screen.blit(button_text, button_text_rect)
        
        # Draw start button
        start_color = self.BUTTON_HOVER_COLOR if self.start_button.collidepoint(mouse_pos) else self.BUTTON_COLOR
        
        # Main button
        pygame.draw.rect(self.screen, start_color, self.start_button, border_radius=12)
        pygame.draw.rect(self.screen, (255, 255, 255, 100), self.start_button, width=2, border_radius=12)
        
        # Button text
        start_text = self.button_font.render("Start Game", True, self.BUTTON_TEXT_COLOR)
        start_text_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, start_text_rect)
    
    def handle_event(self, event):
        """Handle mouse clicks.
        
        Args:
            event: The pygame event
            
        Returns:
            dict with player choice and difficulty if start was clicked, None otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check color selection
            if self.play_as_white_button.collidepoint(event.pos):
                self.player_color = "white"
                return None
            elif self.play_as_black_button.collidepoint(event.pos):
                self.player_color = "black"
                return None
            
            # Check difficulty selection
            for i, button in enumerate(self.difficulty_buttons):
                if button.collidepoint(event.pos):
                    self.difficulty = i + 1
                    return None
            
            # Check start button
            if self.start_button.collidepoint(event.pos):
                from src.logic_engine.player import Player
                
                player_color = Player.WHITE if self.player_color == "white" else Player.BLACK
                return {
                    "player_color": player_color,
                    "difficulty": self.difficulty,
                    "use_logic_ai": True  # Flag to use the logic-based AI
                }
        
        return None
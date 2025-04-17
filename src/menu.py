"""
Menu system for the chess game
"""

import pygame
from src.constants import WIDTH, HEIGHT, FPS, WHITE, BLACK, LIGHT_SQUARE, DARK_SQUARE

class Button:
    """Button class for menu interactions"""
    def __init__(self, text, x, y, width, height, color, hover_color, text_color=BLACK, font_size=24):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.rect = pygame.Rect(x, y, width, height)
        self.selected = False
        
    def draw(self, screen):
        """Draw the button on the screen"""
        mouse_pos = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse_pos)
        
        # Choose color based on hover state and selection state
        if self.selected:
            # Selected state takes precedence
            color = self.hover_color
        elif hover:
            # Hover state
            color = self.hover_color
        else:
            # Normal state
            color = self.color
        
        pygame.draw.rect(screen, color, self.rect)
        
        # Draw border
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw text
        font = pygame.font.SysFont('Arial', self.font_size)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    def is_clicked(self, pos):
        """Check if button is clicked"""
        return self.rect.collidepoint(pos)

class MainMenu:
    """Main menu screen with options to select side and difficulty"""
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.player_color = 'white'
        self.difficulty = 3  # Default: medium
        
        # Sử dụng màu từ constants
        from src.constants import LIGHT_SQUARE, DARK_SQUARE, SELECTED_COLOR, BTN_COLOR, BTN_HOVER_COLOR
        
        self.primary_color = LIGHT_SQUARE  # Màu nền chính
        self.secondary_color = DARK_SQUARE  # Màu nền phụ
        self.selected_color = SELECTED_COLOR  # Màu khi được chọn (xanh lá)
        self.btn_color = BTN_COLOR  # Màu nút (xám nhạt)
        self.btn_hover_color = BTN_HOVER_COLOR  # Màu nút khi hover
        
        # Button dimensions and spacing
        btn_width, btn_height = 200, 50
        btn_margin = 20
        
        # Center position calculations
        center_x = WIDTH // 2
        
        # Row 1: Play as White/Black buttons (side by side)
        white_x = center_x - btn_width - btn_margin // 2
        black_x = center_x + btn_margin // 2
        
        # Increased distance between sections
        side_y = 180
        diff_y = 320  # Tăng khoảng cách giữa phần bên và độ khó
        start_y = 460  # Tăng khoảng cách giữa độ khó và nút Start Game
        
        # Row 2: Difficulty buttons (side by side)
        btn_small_width = (btn_width * 2 + btn_margin) // 3 - btn_margin // 3
        easy_x = center_x - btn_small_width * 1.5 - btn_margin
        medium_x = center_x - btn_small_width // 2
        hard_x = center_x + btn_small_width // 2 + btn_margin
        
        # Create buttons with minimalistic colors
        self.white_btn = Button("Play as White", white_x, side_y, btn_width, btn_height, 
                              self.btn_color, self.selected_color)
        self.black_btn = Button("Play as Black", black_x, side_y, btn_width, btn_height, 
                              self.btn_color, self.selected_color, BLACK)
        
        # Difficulty buttons
        self.easy_btn = Button("Easy", easy_x, diff_y, btn_small_width, btn_height, 
                             self.btn_color, self.selected_color)
        self.medium_btn = Button("Medium", medium_x, diff_y, btn_small_width, btn_height, 
                               self.btn_color, self.selected_color)
        self.hard_btn = Button("Hard", hard_x, diff_y, btn_small_width, btn_height, 
                             self.btn_color, self.selected_color)
        
        # Start button
        self.start_btn = Button("Start Game", center_x - btn_width // 2, start_y, btn_width, btn_height, 
                              self.selected_color, self.btn_hover_color)
        
        # Set initial selection
        self.white_btn.selected = True
        self.medium_btn.selected = True
    
    def handle_events(self):
        """Handle events for the main menu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return {'action': 'quit'}
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle button clicks
                mouse_pos = pygame.mouse.get_pos()
                
                if self.white_btn.is_clicked(mouse_pos):
                    self.player_color = 'white'
                    self.white_btn.selected = True
                    self.black_btn.selected = False
                elif self.black_btn.is_clicked(mouse_pos):
                    self.player_color = 'black'
                    self.white_btn.selected = False
                    self.black_btn.selected = True
                elif self.easy_btn.is_clicked(mouse_pos):
                    self.difficulty = 2
                    self.easy_btn.selected = True
                    self.medium_btn.selected = False
                    self.hard_btn.selected = False
                elif self.medium_btn.is_clicked(mouse_pos):
                    self.difficulty = 3
                    self.easy_btn.selected = False
                    self.medium_btn.selected = True
                    self.hard_btn.selected = False
                elif self.hard_btn.is_clicked(mouse_pos):
                    self.difficulty = 4
                    self.easy_btn.selected = False
                    self.medium_btn.selected = False
                    self.hard_btn.selected = True
                elif self.start_btn.is_clicked(mouse_pos):
                    self.running = False
                    return {'action': 'start', 'player_color': self.player_color, 'difficulty': self.difficulty}
        
        return {'action': 'none'}
    
    def draw(self):
        """Draw the main menu"""
        # Fill background
        self.screen.fill(self.primary_color)  # Sử dụng màu nền từ constants
        
        # Draw title
        font = pygame.font.SysFont('Arial', 48)
        title = font.render("Chess Game with AI", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Draw section titles
        font = pygame.font.SysFont('Arial', 32)
        color_title = font.render("Choose Your Side", True, BLACK)
        color_rect = color_title.get_rect(center=(WIDTH // 2, 140))
        self.screen.blit(color_title, color_rect)
        
        diff_title = font.render("Select Difficulty", True, BLACK)
        diff_rect = diff_title.get_rect(center=(WIDTH // 2, 280))
        self.screen.blit(diff_title, diff_rect)
        
        # Draw buttons
        self.white_btn.draw(self.screen)
        self.black_btn.draw(self.screen)
        self.easy_btn.draw(self.screen)
        self.medium_btn.draw(self.screen)
        self.hard_btn.draw(self.screen)
        self.start_btn.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """Run the main menu loop"""
        result = {'action': 'none'}
        
        while self.running:
            self.clock.tick(FPS)
            event_result = self.handle_events()
            
            if event_result['action'] != 'none':
                result = event_result
                if result['action'] == 'quit':
                    return result
            
            self.draw()
        
        return result

class PauseMenu:
    """Pause menu during gameplay"""
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Sử dụng màu từ constants
        from src.constants import LIGHT_SQUARE, DARK_SQUARE, SELECTED_COLOR, BTN_COLOR, BTN_HOVER_COLOR, OVERLAY_COLOR
        
        self.primary_color = LIGHT_SQUARE  # Màu nền chính
        self.secondary_color = DARK_SQUARE  # Màu nền phụ
        self.selected_color = SELECTED_COLOR  # Màu khi được chọn (xanh lá)
        self.btn_color = BTN_COLOR  # Màu nút (xám nhạt)
        self.btn_hover_color = BTN_HOVER_COLOR  # Màu nút khi hover
        self.overlay_color = OVERLAY_COLOR  # Màu overlay (đen mờ)
        
        # Create buttons
        btn_width, btn_height = 200, 50
        btn_margin = 15
        center_x = WIDTH // 2 - btn_width // 2
        start_y = HEIGHT // 2 - 40
        
        self.resume_btn = Button("Resume", center_x, start_y, btn_width, btn_height,
                               self.btn_color, self.selected_color)
        self.restart_btn = Button("Restart", center_x, start_y + btn_height + btn_margin, btn_width, btn_height,
                                self.btn_color, self.selected_color)
        self.main_menu_btn = Button("Main Menu", center_x, start_y + (btn_height + btn_margin) * 2, btn_width, btn_height,
                                  self.btn_color, self.selected_color)
        self.quit_btn = Button("Quit Game", center_x, start_y + (btn_height + btn_margin) * 3, btn_width, btn_height,
                             self.btn_color, self.selected_color)
    
    def handle_events(self):
        """Handle events for the pause menu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return {'action': 'quit'}
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return {'action': 'resume'}
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.resume_btn.is_clicked(mouse_pos):
                    self.running = False
                    return {'action': 'resume'}
                elif self.restart_btn.is_clicked(mouse_pos):
                    self.running = False
                    return {'action': 'restart'}
                elif self.main_menu_btn.is_clicked(mouse_pos):
                    self.running = False
                    return {'action': 'main_menu'}
                elif self.quit_btn.is_clicked(mouse_pos):
                    self.running = False
                    return {'action': 'quit'}
        
        return {'action': 'none'}
    
    def draw(self):
        """Draw the pause menu overlay"""
        # Vẽ container chính của menu
        container_width = WIDTH
        container_height = HEIGHT
        container_x = WIDTH // 2 - container_width // 2
        container_y = HEIGHT // 2 - container_height // 2

        container_rect = pygame.Rect(container_x, container_y, container_width, container_height)
        pygame.draw.rect(self.screen, self.primary_color, container_rect)

        # Vẽ tiêu đề
        font = pygame.font.SysFont('Arial', 36)
        title = font.render("Paused", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, container_y + 40))
        self.screen.blit(title, title_rect)

        # Vẽ các nút
        self.resume_btn.draw(self.screen)
        self.restart_btn.draw(self.screen)
        self.main_menu_btn.draw(self.screen)
        self.quit_btn.draw(self.screen)

        pygame.display.flip()
    
    def run(self):
        """Run the pause menu loop"""
        # Initial draw
        self.draw()
        
        while self.running:
            self.clock.tick(FPS)
            event_result = self.handle_events()
            
            if event_result['action'] != 'none':
                return event_result
            
            self.draw()
        
        return {'action': 'resume'}

class PromotionMenu:
    """Menu for selecting promotion piece when a pawn reaches the end"""
    def __init__(self, screen, position, color):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.position = position  # Position of the pawn
        self.color = color  # Color of the pawn
        
        # Sử dụng màu từ constants
        from src.constants import LIGHT_SQUARE, SELECTED_COLOR, BTN_COLOR, OVERLAY_COLOR
        
        self.primary_color = LIGHT_SQUARE  # Màu nền chính
        self.btn_color = BTN_COLOR  # Màu nút (xám nhạt)
        self.selected_color = SELECTED_COLOR  # Màu khi được chọn (xanh lá)
        self.overlay_color = OVERLAY_COLOR  # Màu overlay (đen mờ)
        
        # Create buttons for each piece option
        self.options = ['Q', 'R', 'B', 'N']
        self.buttons = []
        
        button_size = 60
        start_x = WIDTH // 2 - (button_size * 2)
        y = HEIGHT // 2 - button_size // 2
        
        for i, piece in enumerate(self.options):
            x = start_x + (i * button_size)
            self.buttons.append(Button(piece, x, y, button_size, button_size, 
                                     self.btn_color, self.selected_color))
    
    def handle_events(self):
        """Handle events for the promotion menu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return {'action': 'quit', 'piece': 'Q'}  # Default to Queen
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                for i, button in enumerate(self.buttons):
                    if button.is_clicked(mouse_pos):
                        self.running = False
                        return {'action': 'promote', 'piece': self.options[i]}
        
        return {'action': 'none'}
    
    def draw(self):
        """Draw the promotion menu overlay"""
        # Lưu bản sao của màn hình hiện tại
        current_screen = self.screen.copy()
        
        # Tạo overlay đen mờ toàn màn hình
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))  # Màu đen
        overlay.set_alpha(180)  # Đặt độ mờ
        self.screen.blit(overlay, (0, 0))
        
        # Draw promotion menu background
        menu_width = 250
        menu_height = 150
        menu_rect = pygame.Rect(WIDTH // 2 - menu_width // 2, HEIGHT // 2 - menu_height // 2,
                              menu_width, menu_height)
        pygame.draw.rect(self.screen, self.primary_color, menu_rect)
        pygame.draw.rect(self.screen, BLACK, menu_rect, 3)
        
        # Draw title
        font = pygame.font.SysFont('Arial', 24)
        title = font.render("Choose promotion piece:", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.screen.blit(title, title_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """Run the promotion menu loop"""
        self.draw()
        
        while self.running:
            self.clock.tick(FPS)
            event_result = self.handle_events()
            
            if event_result['action'] != 'none':
                return event_result
            
            self.draw()
        
        # Default to Queen
        return {'action': 'promote', 'piece': 'Q'}

class GameOverMenu:
    """Game over menu showing results and options"""
    def __init__(self, screen, result):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.result = result  # 'white_wins', 'black_wins', hoặc các loại hòa
        
        # Sử dụng màu từ constants
        from src.constants import LIGHT_SQUARE, SELECTED_COLOR, BTN_COLOR, OVERLAY_COLOR
        
        self.primary_color = LIGHT_SQUARE  # Màu nền chính
        self.btn_color = BTN_COLOR  # Màu nút (xám nhạt)
        self.selected_color = SELECTED_COLOR  # Màu khi được chọn (xanh lá)
        self.overlay_color = OVERLAY_COLOR  # Màu overlay (đen mờ)
        
        # Create buttons
        btn_width, btn_height = 200, 50
        btn_margin = 15
        center_x = WIDTH // 2 - btn_width // 2
        start_y = HEIGHT // 2 + 50
        
        self.play_again_btn = Button("Play Again", center_x, start_y, btn_width, btn_height,
                                   self.btn_color, self.selected_color)
        self.main_menu_btn = Button("Main Menu", center_x, start_y + btn_height + btn_margin, btn_width, btn_height,
                                  self.btn_color, self.selected_color)
        self.quit_btn = Button("Quit Game", center_x, start_y + (btn_height + btn_margin) * 2, btn_width, btn_height,
                             self.btn_color, self.selected_color)
    
    def handle_events(self):
        """Handle events for the game over menu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return {'action': 'quit'}
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.play_again_btn.is_clicked(mouse_pos):
                    self.running = False
                    return {'action': 'restart'}
                elif self.main_menu_btn.is_clicked(mouse_pos):
                    self.running = False
                    return {'action': 'main_menu'}
                elif self.quit_btn.is_clicked(mouse_pos):
                    self.running = False
                    return {'action': 'quit'}
        
        return {'action': 'none'}
    
    def draw(self):
        """Draw the game over menu overlay"""
        # Lưu bản sao của màn hình hiện tại
        current_screen = self.screen.copy()
        
        # Tạo overlay đen mờ toàn màn hình
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))  # Màu đen
        overlay.set_alpha(180)  # Đặt độ mờ
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over menu background
        container_width = 400
        container_height = 350
        container_x = WIDTH // 2 - container_width // 2
        container_y = HEIGHT // 2 - container_height // 2
        
        container_rect = pygame.Rect(container_x, container_y, container_width, container_height)
        pygame.draw.rect(self.screen, self.primary_color, container_rect)
        pygame.draw.rect(self.screen, BLACK, container_rect, 3)
        
        # Draw title
        font = pygame.font.SysFont('Arial', 48)
        title = font.render("Game Over", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, container_y + 60))
        self.screen.blit(title, title_rect)
        
        # Draw result
        font = pygame.font.SysFont('Arial', 36)
        if self.result == 'white_wins':
            result_text = "White Wins!"
        elif self.result == 'black_wins':
            result_text = "Black Wins!"
        elif self.result == 'draw_stalemate':
            result_text = "Draw by Stalemate"
        elif self.result == 'draw_insufficient':
            result_text = "Draw by Insufficient Material"
        elif self.result == 'draw_repetition':
            result_text = "Draw by Threefold Repetition"
        elif self.result == 'draw_fifty_move':
            result_text = "Draw by Fifty-Move Rule"
        else:
            result_text = "Draw!"
        
        result = font.render(result_text, True, BLACK)
        result_rect = result.get_rect(center=(WIDTH // 2, container_y + 120))
        self.screen.blit(result, result_rect)
        
        # Draw buttons
        self.play_again_btn.draw(self.screen)
        self.main_menu_btn.draw(self.screen)
        self.quit_btn.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        """Run the game over menu loop"""
        self.draw()
        
        while self.running:
            self.clock.tick(FPS)
            event_result = self.handle_events()
            
            if event_result['action'] != 'none':
                return event_result
            
            self.draw()
        
        return {'action': 'quit'}
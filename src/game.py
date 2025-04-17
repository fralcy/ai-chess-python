"""
Game management using logical programming approach
"""

import pygame
import time
from src.constants import DARK_SQUARE, FPS, HEADER_HEIGHT, HIGHLIGHT, LIGHT_SQUARE, MOVE_HIGHLIGHT, WIDTH, HEIGHT, BLACK, WHITE, SQUARE_SIZE
from src.board import create_game_state, draw_board, select_piece, move_piece
from src.ai import find_best_move
from src.pieces import is_check, is_checkmate, is_stalemate
from src.menu import MainMenu, PauseMenu, PromotionMenu, GameOverMenu
from src.assets import load_piece_image

class Game:
    """Main game class to manage the chess game"""
    
    def __init__(self, screen):
        """Initialize the game"""
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_active = False
        self.game_over = False
        self.promotion_pending = False
        
        # Game state will be created when game starts
        self.game_state = None
        
        # Default settings
        self.player_color = 'white'
        self.ai_thinking = False
        self.ai_difficulty = 3  # Depth (1: easy, 3: medium, 5: hard)
        
        # Open main menu
        self.show_main_menu()
        
    def show_main_menu(self):
        """Show the main menu to select options"""
        main_menu = MainMenu(self.screen)
        result = main_menu.run()
        
        if result['action'] == 'quit':
            self.running = False
        elif result['action'] == 'start':
            self.player_color = result['player_color']
            self.ai_difficulty = result['difficulty']
            self.start_new_game()
            
    def start_new_game(self):
        """Start a new game with current settings"""
        self.game_state = create_game_state()
        self.game_active = True
        self.game_over = False
        self.promotion_pending = False
        
        # If player is black, let AI make the first move
        if self.player_color == 'black':
            self.ai_thinking = True
        
    def show_pause_menu(self):
        """Show the pause menu"""
        pause_menu = PauseMenu(self.screen)
        result = pause_menu.run()
        
        if result['action'] == 'quit':
            self.running = False
        elif result['action'] == 'main_menu':
            self.game_active = False
            self.show_main_menu()
        elif result['action'] == 'restart':
            self.start_new_game()
    
    def show_promotion_menu(self, position, color):
        """Show the promotion menu when a pawn reaches the end"""
        self.promotion_pending = True
        promotion_menu = PromotionMenu(self.screen, position, color)
        result = promotion_menu.run()
        self.promotion_pending = False
        
        if result['action'] == 'quit':
            self.running = False
        elif result['action'] == 'promote':
            # Update the pawn to the selected piece
            row, col = position
            self.game_state['board'][position] = (result['piece'], color)
    
    def show_game_over_menu(self, result):
        """Show the game over menu"""
        game_over_menu = GameOverMenu(self.screen, result)
        menu_result = game_over_menu.run()
        
        if menu_result['action'] == 'quit':
            self.running = False
        elif menu_result['action'] == 'main_menu':
            self.game_active = False
            self.show_main_menu()
        elif menu_result['action'] == 'restart':
            self.start_new_game()
        
    def handle_mouse_click(self, pos):
        """Handle mouse click event during gameplay"""
        # If promotion is pending or game is over, ignore clicks
        if self.promotion_pending or self.game_over:
            return
            
        # If it's AI's turn, ignore clicks
        if self.game_state['turn'] != self.player_color:
            return
            
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        click_pos = (row, col)
        
        selected = self.game_state['selected_piece']
        valid_moves = self.game_state['valid_moves']
        
        if selected:
            # If a piece is already selected, try to move it
            if click_pos in valid_moves:
                piece = self.game_state['board'].get(selected)
                
                # Check for pawn promotion
                if piece and piece[0] == 'P':
                    end_row = click_pos[0]
                    if (piece[1] == 'white' and end_row == 0) or (piece[1] == 'black' and end_row == 7):
                        # Store the move for after promotion selection
                        self.pending_move = (selected, click_pos)
                        self.show_promotion_menu(click_pos, piece[1])
                        return
                
                # Normal move
                self.game_state = move_piece(self.game_state, selected, click_pos)
                
                # After player's move, check for game over conditions
                self.check_game_over()
                
                # If game continues, let AI think
                if not self.game_over:
                    self.ai_thinking = True
            else:
                # If clicked on another piece of same color, select it
                # Otherwise, deselect current piece
                self.game_state = select_piece(self.game_state, click_pos)
        else:
            # No piece selected, try to select one
            self.game_state = select_piece(self.game_state, click_pos)
    
    def check_game_over(self):
        """Check if the game is over"""
        if not self.game_state:
            return
            
        board = self.game_state['board']
        current_color = self.game_state['turn']
        
        # Import các hàm kiểm tra hòa cờ
        from src.endgame import is_insufficient_material, is_threefold_repetition, is_fifty_move_rule
        
        # Check for checkmate
        if is_checkmate(board, self.game_state, current_color):
            winner = 'black' if current_color == 'white' else 'white'
            self.game_over = True
            self.show_game_over_menu(f"{winner}_wins")
            return True
            
        # Check for stalemate
        if is_stalemate(board, self.game_state, current_color):
            self.game_over = True
            self.show_game_over_menu('draw_stalemate')
            return True
        
        # Check for insufficient material
        if is_insufficient_material(board):
            self.game_over = True
            self.show_game_over_menu('draw_insufficient')
            return True
        
        # Check for threefold repetition
        if is_threefold_repetition(self.game_state):
            self.game_over = True
            self.show_game_over_menu('draw_repetition')
            return True
        
        # Check for fifty move rule
        if is_fifty_move_rule(self.game_state):
            self.game_over = True
            self.show_game_over_menu('draw_fifty_move')
            return True
            
        return False
            
    def make_ai_move(self):
        """Let the AI make a move"""
        if self.ai_thinking and self.game_state and self.game_state['turn'] != self.player_color:
            # Add a slight delay to create the feeling of "thinking"
            time.sleep(0.5)
            
            # Find the best move based on difficulty
            best_move = find_best_move(self.game_state, self.ai_difficulty)
            
            if best_move:
                start, end = best_move
                self.game_state = move_piece(self.game_state, start, end)
                
                # Check for game over after AI move
                self.check_game_over()
            
            self.ai_thinking = False
    
    def draw_game_header(self):
        """Draw the game header showing current turn and status"""
        # Create header background
        header_height = HEADER_HEIGHT
        header_rect = pygame.Rect(0, 0, WIDTH, header_height)
        pygame.draw.rect(self.screen, WHITE, header_rect)
        pygame.draw.line(self.screen, BLACK, (0, header_height), (WIDTH, header_height), 2)
        
        # Chia header thành 3 phần
        font = pygame.font.SysFont('Arial', 20)
        
        # 1. Bên trái: Hiển thị "You're playing as white/black"
        player_text = f"You're playing as {self.player_color}"
        player_surface = font.render(player_text, True, BLACK)
        self.screen.blit(player_surface, (20, 15))
        
        # 2. Ở giữa: Kiểm tra và hiển thị "White/Black is in check" nếu có
        if self.game_state and is_check(self.game_state['board'], self.game_state, self.game_state['turn']):
            current_color = self.game_state['turn'].capitalize()
            check_text = f"{current_color} is in check!"
            check_surface = font.render(check_text, True, (255, 0, 0))
            check_rect = check_surface.get_rect(center=(WIDTH // 2, header_height // 2))
            self.screen.blit(check_surface, check_rect)
        
        # 3. Bên phải: Nút tạm dừng (pause button)
        pause_btn = pygame.Rect(WIDTH - 50, 10, 30, 30)
        pygame.draw.rect(self.screen, (200, 200, 200), pause_btn)
        pygame.draw.rect(self.screen, BLACK, pause_btn, 2)
        
        # Vẽ biểu tượng tạm dừng (hai vạch dọc)
        pygame.draw.rect(self.screen, BLACK, (WIDTH - 45, 15, 8, 20))
        pygame.draw.rect(self.screen, BLACK, (WIDTH - 33, 15, 8, 20))
        
        return pause_btn
        
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.game_active:
                    self.show_pause_menu()
            
            elif event.type == pygame.MOUSEBUTTONDOWN and self.game_active:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if clicked on pause button
                if mouse_pos[1] < 50 and mouse_pos[0] > WIDTH - 50:
                    self.show_pause_menu()
                else:
                    # Handle chess board clicks
                    # If clicking below the header
                    if mouse_pos[1] > 50:
                        # Adjust y coordinate for the header offset
                        adjusted_pos = (mouse_pos[0], mouse_pos[1] - 50)
                        self.handle_mouse_click(adjusted_pos)
    
    def draw(self):
        """Draw the game screen"""
        # Clear screen
        self.screen.fill(BLACK)
        
        if self.game_active and self.game_state:
            # Draw header
            pause_btn = self.draw_game_header()
            
            # Offset the board to account for header
            offset_y = HEADER_HEIGHT
            
            # Draw the chess board with offset
            for row in range(8):
                for col in range(8):
                    color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                    pygame.draw.rect(
                        self.screen, 
                        color, 
                        pygame.Rect(
                            col * SQUARE_SIZE,
                            row * SQUARE_SIZE + offset_y,
                            SQUARE_SIZE,
                            SQUARE_SIZE
                        )
                    )
            
            # Draw pieces
            board = self.game_state['board']
            for pos, piece in board.items():
                row, col = pos
                piece_type, color = piece
                
                # Get piece image
                piece_img = load_piece_image(piece_type, color)
                
                # Calculate position
                piece_rect = piece_img.get_rect(
                    center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                            row * SQUARE_SIZE + SQUARE_SIZE // 2 + offset_y))
                
                # Draw piece
                self.screen.blit(piece_img, piece_rect)
                
            # Highlight selected piece
            selected = self.game_state['selected_piece']
            if selected:
                row, col = selected
                highlight_rect = pygame.Rect(
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE + offset_y,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
                highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight_surface.fill(HIGHLIGHT)
                self.screen.blit(highlight_surface, highlight_rect)
                
            # Highlight valid moves
            valid_moves = self.game_state['valid_moves']
            for move in valid_moves:
                row, col = move
                move_rect = pygame.Rect(
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE + offset_y,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
                move_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                move_surface.fill(MOVE_HIGHLIGHT)
                self.screen.blit(move_surface, move_rect)
        
        # Update display
        pygame.display.flip()
        
    def run(self):
        """Main game loop"""
        while self.running:
            # Control game speed
            self.clock.tick(FPS)
            
            # Handle events
            self.handle_events()
            
            # Make AI move if needed
            if self.game_active and self.ai_thinking and not self.game_over:
                self.make_ai_move()
            
            # Draw the game
            self.draw()
"""
Game management using logical programming approach
"""

import pygame
from src.constants import FPS, WIDTH, HEIGHT, BLACK, SQUARE_SIZE
from src.board import create_game_state, draw_board, select_piece, move_piece
from src.ai import find_best_move

class Game:
    """Main game class to manage the chess game"""
    
    def __init__(self, screen):
        """Initialize the game"""
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = create_game_state()
        self.player_color = 'white'  # Người chơi mặc định là bên trắng
        self.ai_thinking = False
        
    def handle_mouse_click(self, pos):
        """Handle mouse click event"""
        # Nếu đang là lượt của AI, bỏ qua click
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
                self.game_state = move_piece(self.game_state, selected, click_pos)
                # Sau khi người chơi di chuyển, đến lượt AI
                self.ai_thinking = True
            else:
                # If clicked on another piece of same color, select it
                # Otherwise, deselect current piece
                self.game_state = select_piece(self.game_state, click_pos)
        else:
            # No piece selected, try to select one
            self.game_state = select_piece(self.game_state, click_pos)
    
    def make_ai_move(self):
        """Let the AI make a move"""
        if self.ai_thinking and self.game_state['turn'] != self.player_color:
            best_move = find_best_move(self.game_state)
            if best_move:
                start, end = best_move
                self.game_state = move_piece(self.game_state, start, end)
            self.ai_thinking = False
        
    def run(self):
        """Main game loop"""
        while self.running:
            # Control game speed
            self.clock.tick(FPS)
            
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.handle_mouse_click(mouse_pos)
            
            # AI's turn
            self.make_ai_move()
            
            # Draw background
            self.screen.fill(BLACK)
            
            # Draw the board
            draw_board(self.screen, self.game_state)
            
            # Update the display
            pygame.display.flip()
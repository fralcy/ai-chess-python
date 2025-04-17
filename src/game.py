"""
Game management using logical programming approach
"""

import pygame
from src.constants import FPS, WIDTH, HEIGHT, BLACK
from src.board import create_game_state, draw_board

class Game:
    """Main game class to manage the chess game"""
    
    def __init__(self, screen):
        """Initialize the game"""
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = create_game_state()
        
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
                    # Sẽ được bổ sung trong commit tiếp theo
                    pass
            
            # Draw background
            self.screen.fill(BLACK)
            
            # Draw the board
            draw_board(self.screen, self.game_state)
            
            # Update the display
            pygame.display.flip()
"""
Game management class
"""

import pygame
from src.constants import FPS

class Game:
    """Main game class to manage the chess game"""
    
    def __init__(self, screen):
        """Initialize the game"""
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
    def run(self):
        """Main game loop"""
        while self.running:
            # Control game speed
            self.clock.tick(FPS)
            
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Draw background
            self.screen.fill((0, 0, 0))
            
            # Update the display
            pygame.display.flip()
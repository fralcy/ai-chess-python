"""
Chess Game with AI using Minimax Algorithm
Main entry point for the application
"""

import pygame
from src.game import Game
from src.constants import WIDTH, HEIGHT, TITLE

def main():
    """Main function to run the chess game"""
    # Initialize pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    
    # Create and run the game
    game = Game(screen)
    game.run()
    
    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()
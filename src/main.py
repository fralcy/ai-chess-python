import pygame
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.chess_board import ChessBoard

def ensure_assets_directory():
    """Ensure the assets directory exists for the chess piece images."""
    # Create assets/images directory if it doesn't exist
    if not os.path.exists('assets/images'):
        os.makedirs('assets/images', exist_ok=True)
        print("Created assets/images directory for chess piece images")
        print("Please add chess piece images to this directory before running the game")
        print("Expected filenames: white_pawn.png, black_king.png, etc.")

def main():
    # Ensure assets directory exists
    ensure_assets_directory()
    
    # Initialize pygame
    pygame.init()
    
    # Set up the display
    SQUARE_SIZE = 80
    BOARD_SIZE = SQUARE_SIZE * 8
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption("Chess Game")
    
    # Create chess board
    chess_board = ChessBoard(screen)
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # Fill the screen with a background color
        screen.fill((0, 0, 0))
        
        # Draw the chess board and pieces
        chess_board.draw()
        
        # Update the display
        pygame.display.flip()
        
        # Cap the framerate
        clock.tick(60)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
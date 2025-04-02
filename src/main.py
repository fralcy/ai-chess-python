import pygame
import sys
import os
from ui.ai_menu import AIMenu

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.chess_board import ChessBoard
from ui.game_over_menu import GameOverMenu  # Import the new GameOverMenu class
from logic.player import Player
from logic.end_reason import EndReason

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
    STATUS_BAR_HEIGHT = 30  # Chiều cao của thanh trạng thái
    
    # Tạo cửa sổ với chiều cao bao gồm cả thanh trạng thái
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + STATUS_BAR_HEIGHT))
    pygame.display.set_caption("Chess Game")

    # Tạo menu AI
    ai_menu = AIMenu(screen)
    show_ai_menu = True  # Hiển thị menu AI khi bắt đầu

    # Create chess board
    chess_board = ChessBoard(screen)
    
    # Create game over menu (initially with no values)
    game_over_menu = None
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if chess_board and not show_ai_menu:
                        chess_board.toggle_pause()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if show_ai_menu:
                        # Xử lý sự kiện trên menu AI
                        result = ai_menu.handle_event(event)
                        if result:
                            # Người dùng đã chọn xong, khởi tạo bàn cờ
                            chess_board = ChessBoard(screen)
                            # Thiết lập trò chơi với AI
                            chess_board.setup_ai_game(
                                result["player_color"],
                                result["difficulty"]
                            )
                            show_ai_menu = False
                    elif chess_board:
                        # Xử lý click trên bàn cờ
                        pause_result = chess_board.handle_pause_menu_event(event)
                        if pause_result == True:
                            continue
                        elif pause_result == "AI_MENU":
                            # Người chơi muốn quay về menu AI
                            show_ai_menu = True
                            chess_board = None
                            game_over_menu = None
                            continue
                        
                        if game_over_menu is not None:  # Xử lý click trên GameOverMenu
                            if game_over_menu.handle_restart_click(event):
                                # Quay về menu AI khi bắt đầu lại
                                show_ai_menu = True
                                chess_board = None
                                game_over_menu = None
                            elif game_over_menu.handle_exit_click(event):
                                running = False
                        elif not chess_board.is_paused:  # Chỉ xử lý click trên bàn cờ khi không tạm dừng
                            chess_board.handle_click(event.pos)

        # Fill the screen with a background color
        screen.fill((0, 0, 0))
        
        if show_ai_menu:
            # Hiển thị menu AI
            ai_menu.draw()
        else:
            # Hiển thị bàn cờ
            chess_board.draw()
        
            # Check if game has ended
            if chess_board and chess_board.game_state.is_game_over() and game_over_menu is None:
                result = chess_board.game_state.result
                game_over_menu = GameOverMenu(screen, chess_board.game_state)
        
            # Draw game over menu if game has ended
            if game_over_menu is not None:
                game_over_menu.draw()
        
        # Update the display
        pygame.display.flip()
        
        # Cap the framerate
        clock.tick(60)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
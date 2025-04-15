import pygame
import sys
import os
from logic_engine.ai.ai_player import LogicAIPlayer
import threading
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_engine.logic_board import LogicBoard as Board
from logic_engine.logic_game_state import LogicGameState as GameState
from logic_engine.player import Player
from logic_engine.piece_type import PieceType
from logic_engine.position import Position
from ui.promotion_menu import PromotionMenu
from ui.pause_menu import PauseMenu
from ui.option import Option

class ChessBoard:
    # Colors
    LIGHT_SQUARE = (240, 217, 181)  # Beige color for light squares
    DARK_SQUARE = (181, 136, 99)    # Brown color for dark squares
    HIGHLIGHT_COLOR = (124, 252, 0, 128)  # Semi-transparent green for possible moves
    SELECTED_COLOR = (255, 255, 0, 160)   # Semi-transparent yellow for selected piece
    STATUS_BAR_COLOR = (50, 50, 50)  # Dark gray for status bar
    STATUS_TEXT_COLOR = (255, 255, 255)  # White text
    AI_THINKING_COLOR = (255, 165, 0)  # Orange text for "AI thinking..."
    
    # Board dimensions
    SQUARE_SIZE = 80
    BOARD_SIZE = SQUARE_SIZE * 8
    STATUS_BAR_HEIGHT = 30  # Chiều cao thanh trạng thái
    
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.game_state = GameState(self.board, Player.WHITE)
        self.load_pieces_images()
        self.selected_pos = None
        self.possible_moves = []
        self.promotion_menu = None
        self.pause_menu = None
        self.is_paused = False
        self.ai_player = None
        self.ai_thinking = False
        self.player_color = Player.WHITE
        self.use_ai = False
        
        # Tạo font cho thanh trạng thái
        try:
            self.status_font = pygame.font.Font("freesansbold.ttf", 18)
        except:
            self.status_font = pygame.font.SysFont('Arial', 18, bold=True)
    
    def load_pieces_images(self):
        """Load chess piece images."""
        self.piece_images = {}
        pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        colors = ['white', 'black']
        
        for piece in pieces:
            for color in colors:
                image_path = f'assets/images/{color}_{piece}.png'
                try:
                    # Load and scale the image to fit squares
                    img = pygame.image.load(image_path)
                    img = pygame.transform.scale(img, (self.SQUARE_SIZE, self.SQUARE_SIZE))
                    
                    # Create key for the image dictionary
                    piece_type = getattr(PieceType, piece.upper())
                    player = Player.WHITE if color == 'white' else Player.BLACK
                    self.piece_images[(player, piece_type)] = img
                except pygame.error as e:
                    print(f"Cannot load image: {image_path}")
                    print(f"Error: {e}")
    
    def draw_board(self):
        """Draw the chess board with alternating colors."""
        # Create font for labels
        font = pygame.font.SysFont('Arial', 16)
        
        # Vẽ bàn cờ bắt đầu từ vị trí dưới thanh trạng thái
        board_start_y = self.STATUS_BAR_HEIGHT
        
        for row in range(8):
            for col in range(8):
                # Determine square color
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                
                # Draw square
                pygame.draw.rect(
                    self.screen,
                    color,
                    (col * self.SQUARE_SIZE, board_start_y + row * self.SQUARE_SIZE, 
                     self.SQUARE_SIZE, self.SQUARE_SIZE)
                )
                
                # Add row and column labels
                if col == 0:  # Numbers on the left edge (rows)
                    text_color = self.DARK_SQUARE if (row + col) % 2 == 0 else self.LIGHT_SQUARE
                    label = font.render(str(8 - row), True, text_color)
                    self.screen.blit(label, (5, board_start_y + row * self.SQUARE_SIZE + 5))
                
                if row == 7:  # Letters on the bottom edge (columns)
                    text_color = self.DARK_SQUARE if (row + col) % 2 == 0 else self.LIGHT_SQUARE
                    label = font.render(chr(97 + col), True, text_color)  # 'a' through 'h'
                    self.screen.blit(label, (col * self.SQUARE_SIZE + self.SQUARE_SIZE - 15, 
                                           board_start_y + self.BOARD_SIZE - 20))
    
    def draw_pieces(self):
        """Draw pieces on the board according to the current board state."""
        from ui.fallback_renderer import FallbackRenderer
        
        # Vẽ quân cờ bắt đầu từ vị trí dưới thanh trạng thái
        board_start_y = self.STATUS_BAR_HEIGHT
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece:
                    image_key = (piece.color, piece.piece_type)
                    if image_key in self.piece_images:
                        self.screen.blit(
                            self.piece_images[image_key],
                            (col * self.SQUARE_SIZE, board_start_y + row * self.SQUARE_SIZE)
                        )
                    else:
                        # Use fallback renderer if image not available
                        FallbackRenderer.render_piece(
                            self.screen, 
                            piece, 
                            col * self.SQUARE_SIZE, 
                            board_start_y + row * self.SQUARE_SIZE, 
                            self.SQUARE_SIZE
                        )
    
    def draw_highlights(self):
        """Draw highlights for selected piece and possible moves."""
        if self.selected_pos:
            # Create a semi-transparent surface for the highlights
            highlight_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
            
            # Vẽ highlight bắt đầu từ vị trí dưới thanh trạng thái
            board_start_y = self.STATUS_BAR_HEIGHT
            
            # Highlight selected piece
            row, col = self.selected_pos.row, self.selected_pos.column
            pygame.draw.rect(highlight_surface, self.SELECTED_COLOR, 
                           (0, 0, self.SQUARE_SIZE, self.SQUARE_SIZE))
            self.screen.blit(highlight_surface, (col * self.SQUARE_SIZE, board_start_y + row * self.SQUARE_SIZE))
            
            # Highlight possible moves
            highlight_surface.fill((0, 0, 0, 0))  # Clear with transparent color
            pygame.draw.rect(highlight_surface, self.HIGHLIGHT_COLOR, 
                           (0, 0, self.SQUARE_SIZE, self.SQUARE_SIZE))
            
            for move in self.possible_moves:
                to_row, to_col = move.to_pos.row, move.to_pos.column
                self.screen.blit(highlight_surface, (to_col * self.SQUARE_SIZE, board_start_y + to_row * self.SQUARE_SIZE))
    
    def draw_status_bar(self):
        """Vẽ thanh trạng thái hiển thị lượt chơi hiện tại."""
        # Vẽ nền của thanh trạng thái
        pygame.draw.rect(
            self.screen,
            self.STATUS_BAR_COLOR,
            (0, 0, self.BOARD_SIZE, self.STATUS_BAR_HEIGHT)
        )
        
        # Xác định nội dung hiển thị
        if self.game_state.is_game_over():
            # Hiển thị kết quả nếu trò chơi đã kết thúc
            if self.game_state.result.winner == Player.NONE:
                status_text = "Game Over - Draw"
            else:
                winner = "White" if self.game_state.result.winner == Player.WHITE else "Black"
                status_text = f"Game Over - {winner} wins"
        elif self.ai_thinking:
            # Hiển thị "AI thinking..." khi AI đang suy nghĩ
            status_text = "AI thinking..."
            # Vẽ văn bản với màu khác
            status_surface = self.status_font.render(status_text, True, self.AI_THINKING_COLOR)
            status_rect = status_surface.get_rect(center=(self.BOARD_SIZE // 2, self.STATUS_BAR_HEIGHT // 2))
            self.screen.blit(status_surface, status_rect)
            return
        else:
            # Hiển thị lượt của người chơi hiện tại
            current_player = "White" if self.game_state.current_player == Player.WHITE else "Black"
            
            if self.use_ai:
                if self.game_state.current_player == self.player_color:
                    status_text = "Your turn"
                else:
                    status_text = "AI's turn"
            else:
                status_text = f"{current_player}'s turn"
        
        # Vẽ văn bản
        status_surface = self.status_font.render(status_text, True, self.STATUS_TEXT_COLOR)
        status_rect = status_surface.get_rect(center=(self.BOARD_SIZE // 2, self.STATUS_BAR_HEIGHT // 2))
        self.screen.blit(status_surface, status_rect)
    
    def handle_click(self, pos):
        """Handle mouse click on the board."""
        # Nếu đang sử dụng AI và không phải lượt của người chơi thì bỏ qua click
        if self.use_ai and self.game_state.current_player != self.player_color:
            return
        
        # Import MoveType if it's not already imported at the top
        from logic_engine.move_type import MoveType
        
        if self.promotion_menu:  # Handle promotion menu clicks
            selected_piece_type = self.promotion_menu.handle_click(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': pos, 'button': 1}))
            if selected_piece_type:
                # Find the promotion move from possible moves
                promotion_move = next(
                    (move for move in self.possible_moves 
                    if move.type == MoveType.PAWN_PROMOTION),
                    None
                )
                
                if promotion_move:
                    # Create a new promotion move with the selected piece type
                    # Create the promotion move


                    
                    # Execute the promotion move

                    
                    # Reset selection state
                    self.selected_pos = None
                    self.possible_moves = []
                    self.promotion_menu = None  # Close the promotion menu
                    
                    # Gọi AI đi nếu cần
                    if self.use_ai and not self.game_state.is_game_over() and self.game_state.current_player == self.ai_player.player_color:
                        self.make_ai_move()
                return

        # Điều chỉnh vị trí click để tính toán đúng ô trên bàn cờ
        # (trừ đi chiều cao thanh trạng thái)
        adjusted_pos = (pos[0], pos[1] - self.STATUS_BAR_HEIGHT)
        col = adjusted_pos[0] // self.SQUARE_SIZE
        row = adjusted_pos[1] // self.SQUARE_SIZE

        # Make sure we're within the board
        if 0 <= row < 8 and 0 <= col < 8:
            clicked_pos = Position(row, col)
            piece = self.board.get_piece(clicked_pos)

            # If a piece is already selected
            if self.selected_pos:
                # Check if clicked position is in possible moves
                move_executed = False

                        # Check if the move is a promotion

                        # Execute the move


                if move_executed:
                    # Gọi AI đi nếu cần
                    if self.use_ai and not self.game_state.is_game_over() and self.game_state.current_player == self.ai_player.player_color:
                        self.make_ai_move()
                    return

                # If clicked on the same piece, deselect it
                if self.selected_pos == clicked_pos:
                    self.selected_pos = None
                    self.possible_moves = []
                    return

                # If clicked on another piece of same color, select it instead
                if piece and piece.color == self.game_state.current_player:
                    self.selected_pos = clicked_pos
                    self.possible_moves = list(self.game_state.legal_moves_for_piece(clicked_pos))
                    return

                # Otherwise, deselect current piece
                self.selected_pos = None
                self.possible_moves = []

            # If no piece is selected yet and clicked on own piece
            elif piece and piece.color == self.game_state.current_player:
                self.selected_pos = clicked_pos
                self.possible_moves = list(self.game_state.legal_moves_for_piece(clicked_pos))
    
    def draw(self):
        """Draw the complete chess board with pieces and highlights."""
        # Vẽ thanh trạng thái trước
        self.draw_status_bar()
        
        # Sau đó vẽ bàn cờ và các phần tử khác
        self.draw_board()
        self.draw_highlights()
        self.draw_pieces()
        
        if self.promotion_menu:  # Draw promotion menu if active
            self.promotion_menu.draw()
        
        if self.is_paused and self.pause_menu:  # Draw pause menu if active
            self.pause_menu.draw()
    
    def toggle_pause(self):
        """Toggle the pause state of the game."""
        self.is_paused = not self.is_paused
        
        if self.is_paused and not self.pause_menu:
            self.pause_menu = PauseMenu(self.screen)

    def handle_pause_menu_event(self, event):
        """Handle events from the pause menu."""
        if not self.is_paused or not self.pause_menu:
            return False
        
        option = self.pause_menu.handle_event(event)
        if option == Option.CONTINUE:
            self.is_paused = False
            return True
        elif option == Option.RESTART:
            # Khởi tạo lại bàn cờ nhưng giữ nguyên cài đặt AI
            player_color = self.player_color
            use_ai = self.use_ai
            ai_difficulty = self.ai_player.difficulty if self.ai_player else 3
            
            # Khởi tạo lại bàn cờ
            self.__init__(self.screen)
            
            # Thiết lập lại AI nếu cần
            if use_ai:
                self.setup_ai_game(player_color, ai_difficulty)
                
            self.is_paused = False
            return True
        elif option == Option.EXIT:
            # Báo hiệu rằng người chơi muốn quay về AI menu
            return "AI_MENU"
        
        return False
    
    def setup_ai_game(self, player_color, difficulty=3):
        """
        Setup game with AI.
        
        Args:
            player_color: The color of the human player
            difficulty: The difficulty level of the AI (1-5)
        """
        self.player_color = player_color
        self.use_ai = True
        
        # AI will play the opposite color
        ai_color = Player.BLACK if player_color == Player.WHITE else Player.WHITE
        
        # Create the AI player
        self.ai_player = LogicAIPlayer(ai_color, difficulty)
        self.ai_player.set_difficulty(difficulty)
        
        # If AI is White, it will go first
        if ai_color == Player.WHITE:
            self.make_ai_move()

    def make_ai_move(self):
        """Request the AI to find and make the best move."""
        if not self.use_ai or self.ai_player is None:
            return
        
        # Check if it's the AI's turn
        if self.game_state.current_player != self.ai_player.player_color:
            return
        
        # Mark AI as thinking (for UI feedback)
        self.ai_thinking = True
        
        # Create a thread for AI calculation to avoid freezing the UI
        def ai_move_thread():
            try:
                # Let the AI choose a move
                move = self.ai_player.choose_move(self.game_state)
                
                # Execute the move if found

                    # Check if the move is a pawn promotion

                        # Let the AI choose the promotion piece

                        
                        # Create a promotion move with the chosen piece

            finally:
                # Mark AI as done thinking
                self.ai_thinking = False
                
                # Reset selected position and possible moves
                self.selected_pos = None
                self.possible_moves = []
        
        # Create and start the AI thread
        import threading
        ai_thread = threading.Thread(target=ai_move_thread)
        ai_thread.daemon = True  # Auto-terminate thread when the game exits
        ai_thread.start()
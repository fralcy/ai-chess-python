import pygame
import sys
import os
from ai.ai_player import AIPlayer
import threading
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.board import Board
from logic.player import Player
from logic.piece_type import PieceType
from logic.position import Position
from logic.game_state import GameState
from logic.move_type import MoveType
from ui.promotion_menu import PromotionMenu  # Import PromotionMenu
from ui.pause_menu import PauseMenu  # Import PauseMenu
from ui.option import Option

class ChessBoard:
    # Colors
    LIGHT_SQUARE = (240, 217, 181)  # Beige color for light squares
    DARK_SQUARE = (181, 136, 99)    # Brown color for dark squares
    HIGHLIGHT_COLOR = (124, 252, 0, 128)  # Semi-transparent green for possible moves
    SELECTED_COLOR = (255, 255, 0, 160)   # Semi-transparent yellow for selected piece
    
    # Board dimensions
    SQUARE_SIZE = 80
    BOARD_SIZE = SQUARE_SIZE * 8
    
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.game_state = GameState(self.board, Player.WHITE)
        self.load_pieces_images()
        self.selected_pos = None
        self.possible_moves = []
        self.promotion_menu = None  # Add promotion menu state
        self.pause_menu = None  # Initialize to None, will be created when needed
        self.is_paused = False  # Track if the game is paused
        self.ai_player = None
        self.ai_thinking = False
        self.player_color = Player.WHITE  # Màu người chơi mặc định
        self.use_ai = False  # Có sử dụng AI không
        
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
        
        for row in range(8):
            for col in range(8):
                # Determine square color
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                
                # Draw square
                pygame.draw.rect(
                    self.screen,
                    color,
                    (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, 
                     self.SQUARE_SIZE, self.SQUARE_SIZE)
                )
                
                # Add row and column labels
                if col == 0:  # Numbers on the left edge (rows)
                    text_color = self.DARK_SQUARE if (row + col) % 2 == 0 else self.LIGHT_SQUARE
                    label = font.render(str(8 - row), True, text_color)
                    self.screen.blit(label, (5, row * self.SQUARE_SIZE + 5))
                
                if row == 7:  # Letters on the bottom edge (columns)
                    text_color = self.DARK_SQUARE if (row + col) % 2 == 0 else self.LIGHT_SQUARE
                    label = font.render(chr(97 + col), True, text_color)  # 'a' through 'h'
                    self.screen.blit(label, (col * self.SQUARE_SIZE + self.SQUARE_SIZE - 15, 
                                           self.BOARD_SIZE - 20))
    
    def draw_pieces(self):
        """Draw pieces on the board according to the current board state."""
        from ui.fallback_renderer import FallbackRenderer
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece:
                    image_key = (piece.color, piece.piece_type)
                    if image_key in self.piece_images:
                        self.screen.blit(
                            self.piece_images[image_key],
                            (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE)
                        )
                    else:
                        # Use fallback renderer if image not available
                        FallbackRenderer.render_piece(
                            self.screen, 
                            piece, 
                            col * self.SQUARE_SIZE, 
                            row * self.SQUARE_SIZE, 
                            self.SQUARE_SIZE
                        )
    
    def draw_highlights(self):
        """Draw highlights for selected piece and possible moves."""
        if self.selected_pos:
            # Create a semi-transparent surface for the highlights
            highlight_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
            
            # Highlight selected piece
            row, col = self.selected_pos.row, self.selected_pos.column
            pygame.draw.rect(highlight_surface, self.SELECTED_COLOR, 
                           (0, 0, self.SQUARE_SIZE, self.SQUARE_SIZE))
            self.screen.blit(highlight_surface, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
            
            # Highlight possible moves
            highlight_surface.fill((0, 0, 0, 0))  # Clear with transparent color
            pygame.draw.rect(highlight_surface, self.HIGHLIGHT_COLOR, 
                           (0, 0, self.SQUARE_SIZE, self.SQUARE_SIZE))
            
            for move in self.possible_moves:
                to_row, to_col = move.to_pos.row, move.to_pos.column
                self.screen.blit(highlight_surface, (to_col * self.SQUARE_SIZE, to_row * self.SQUARE_SIZE))
    
    def handle_click(self, pos):
        """Handle mouse click on the board."""
        # Nếu đang sử dụng AI và không phải lượt của người chơi thì bỏ qua click
        if self.use_ai and self.game_state.current_player != self.player_color:
            return
        
        # Import MoveType if it's not already imported at the top
        from logic.move_type import MoveType
        
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
                    from logic.moves.pawn_promotion import PawnPromotion
                    updated_move = PawnPromotion(
                        promotion_move.from_pos,
                        promotion_move.to_pos,
                        selected_piece_type
                    )
                    
                    # Execute the promotion move
                    self.game_state.make_move(updated_move)
                    
                    # Reset selection state
                    self.selected_pos = None
                    self.possible_moves = []
                    self.promotion_menu = None  # Close the promotion menu
                    
                    # Gọi AI đi nếu cần
                    if self.use_ai and not self.game_state.is_game_over() and self.game_state.current_player == self.ai_player.player_color:
                        self.make_ai_move()
                return

        col = pos[0] // self.SQUARE_SIZE
        row = pos[1] // self.SQUARE_SIZE

        # Make sure we're within the board
        if 0 <= row < 8 and 0 <= col < 8:
            clicked_pos = Position(row, col)
            piece = self.board.get_piece(clicked_pos)

            # If a piece is already selected
            if self.selected_pos:
                # Check if clicked position is in possible moves
                move_executed = False
                for move in self.possible_moves:
                    if move.to_pos == clicked_pos:
                        # Check if the move is a promotion
                        if move.type == MoveType.PAWN_PROMOTION:
                            self.promotion_menu = PromotionMenu(
                                self.screen,
                                self.game_state.current_player,
                                self.SQUARE_SIZE
                            )
                            return
                        # Execute the move
                        self.game_state.make_move(move)
                        move_executed = True
                        self.selected_pos = None
                        self.possible_moves = []
                        break

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
        self.draw_board()
        self.draw_highlights()
        self.draw_pieces()
        
        if self.promotion_menu:  # Draw promotion menu if active
            self.promotion_menu.draw()
        
        if self.is_paused and self.pause_menu:  # Draw pause menu if active
            self.pause_menu.draw()
        
        # Hiển thị thông báo khi AI đang suy nghĩ
        if self.use_ai and self.ai_thinking:
            # Tạo một overlay bán trong suốt
            overlay = pygame.Surface((50, 30), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (self.BOARD_SIZE - 150, 10))
            
            # Hiển thị thông báo
            font = pygame.font.SysFont('Arial', 16)
            text = font.render("AI thinking...", True, (255, 255, 255))
            self.screen.blit(text, (self.BOARD_SIZE - 140, 15))
    
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
            self.__init__(self.screen)  # Restart the game by reinitializing
            self.is_paused = False
            return True
        
        return False
    
    def setup_ai_game(self, player_color, difficulty=3):
        """
        Thiết lập game với AI.
        
        Args:
            player_color: Màu quân của người chơi
            difficulty: Độ khó của AI (1-5)
        """
        self.player_color = player_color
        self.use_ai = True
        
        # AI sẽ chơi màu đối diện với người chơi
        ai_color = Player.BLACK if player_color == Player.WHITE else Player.WHITE
        
        # Tạo đối tượng AI player
        self.ai_player = AIPlayer(ai_color, difficulty)
        
        # Nếu AI là WHITE, nó sẽ đi trước
        if ai_color == Player.WHITE:
            self.make_ai_move()

    def make_ai_move(self):
        """Yêu cầu AI tìm và thực hiện nước đi tốt nhất."""
        if not self.use_ai or self.ai_player is None:
            return
        
        # Kiểm tra xem hiện tại có phải lượt của AI không
        if self.game_state.current_player != self.ai_player.player_color:
            return
        
        # Đánh dấu AI đang suy nghĩ (để hiển thị thông báo nếu cần)
        self.ai_thinking = True
        
        # Tạo một thread riêng để AI tính toán, không làm đơ giao diện
        def ai_move_thread():
            try:
                # Để AI chọn nước đi
                move = self.ai_player.choose_move(self.game_state)
                
                # Thực hiện nước đi nếu tìm được
                if move:
                    # Kiểm tra xem nước đi có phải là phong cấp tốt không
                    if move.type == MoveType.PAWN_PROMOTION:
                        # Gọi phương thức handle_promotion để AI chọn quân phong cấp
                        promotion_piece = self.ai_player.handle_promotion(
                            self.game_state, move.from_pos, move.to_pos)
                        
                        # Cập nhật nước đi với quân phong cấp đã chọn
                        from logic.moves.pawn_promotion import PawnPromotion
                        updated_move = PawnPromotion(
                            move.from_pos,
                            move.to_pos,
                            promotion_piece
                        )
                        self.game_state.make_move(updated_move)
                    else:
                        self.game_state.make_move(move)
                
            finally:
                # Đánh dấu AI đã nghĩ xong
                self.ai_thinking = False
                
                # Reset selected position và possible moves
                self.selected_pos = None
                self.possible_moves = []
        
        # Tạo và bắt đầu thread
        ai_thread = threading.Thread(target=ai_move_thread)
        ai_thread.daemon = True  # Để thread tự động kết thúc khi thoát game
        ai_thread.start()
import pygame
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.board import Board
from logic.player import Player
from logic.piece_type import PieceType
from logic.position import Position
from logic.game_state import GameState

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
        col = pos[0] // self.SQUARE_SIZE
        row = pos[1] // self.SQUARE_SIZE
        
        # Make sure we're within the board
        if 0 <= row < 8 and 0 <= col < 8:
            clicked_pos = Position(row, col)
            piece = self.board.get_piece(clicked_pos)
            
            # If a piece is already selected
            if self.selected_pos:
                # Check if clicked position is in possible moves
                for move in self.possible_moves:
                    if move.to_pos == clicked_pos:
                        # Execute the move
                        self.game_state.make_move(move)
                        self.selected_pos = None
                        self.possible_moves = []
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
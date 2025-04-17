"""
Chess board representation using logical programming approach
"""

import pygame
from src.constants import BOARD_SIZE, SQUARE_SIZE, LIGHT_SQUARE, DARK_SQUARE

# Biểu diễn bàn cờ như một tập hợp các facts
# Bàn cờ sẽ được biểu diễn dưới dạng dictionary thay vì lớp đối tượng
def create_board():
    """Create an initial chess board state as a set of facts"""
    # Format: board[position] = (piece_type, color)
    # position là tuple (row, col)
    # piece_type: 'P' (pawn), 'R' (rook), 'N' (knight), 'B' (bishop), 'Q' (queen), 'K' (king)
    # color: 'white' hoặc 'black'
    
    board = {}
    
    # Khởi tạo quân trắng
    for col in range(BOARD_SIZE):
        board[(6, col)] = ('P', 'white')  # Các quân tốt
    
    board[(7, 0)] = ('R', 'white')  # Xe trắng
    board[(7, 7)] = ('R', 'white')
    board[(7, 1)] = ('N', 'white')  # Mã trắng
    board[(7, 6)] = ('N', 'white')
    board[(7, 2)] = ('B', 'white')  # Tượng trắng
    board[(7, 5)] = ('B', 'white')
    board[(7, 3)] = ('Q', 'white')  # Hậu trắng
    board[(7, 4)] = ('K', 'white')  # Vua trắng
    
    # Khởi tạo quân đen
    for col in range(BOARD_SIZE):
        board[(1, col)] = ('P', 'black')  # Các quân tốt
    
    board[(0, 0)] = ('R', 'black')  # Xe đen
    board[(0, 7)] = ('R', 'black')
    board[(0, 1)] = ('N', 'black')  # Mã đen
    board[(0, 6)] = ('N', 'black')
    board[(0, 2)] = ('B', 'black')  # Tượng đen
    board[(0, 5)] = ('B', 'black')
    board[(0, 3)] = ('Q', 'black')  # Hậu đen
    board[(0, 4)] = ('K', 'black')  # Vua đen
    
    return board

# Game state dưới dạng facts
def create_game_state():
    """Create initial game state facts"""
    state = {
        'board': create_board(),
        'turn': 'white',
        'white_king_pos': (7, 4),
        'black_king_pos': (0, 4),
        'castling_rights': {
            'white_king_side': True,
            'white_queen_side': True,
            'black_king_side': True,
            'black_queen_side': True
        },
        'en_passant_target': None,
        'move_history': [],
        'selected_piece': None
    }
    return state

# Logical rules
def is_valid_position(pos):
    """Check if position is within board boundaries"""
    row, col = pos
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

def get_piece_at(board, pos):
    """Get piece at the given position"""
    if pos in board:
        return board[pos]
    return None

def is_opponent(piece1, piece2):
    """Check if pieces are opponents"""
    if piece1 is None or piece2 is None:
        return False
    return piece1[1] != piece2[1]

def draw_board(screen, game_state):
    """Draw the chess board and pieces"""
    board = game_state['board']
    selected = game_state['selected_piece']
    
    # Draw the board squares
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Determine square color
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            
            # Draw the square
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
            )
            
            # Highlight selected piece
            if selected and selected == (row, col):
                pygame.draw.rect(
                    screen,
                    (255, 255, 0, 128),  # Yellow with alpha
                    pygame.Rect(
                        col * SQUARE_SIZE,
                        row * SQUARE_SIZE,
                        SQUARE_SIZE,
                        SQUARE_SIZE
                    )
                )
    
    # Draw pieces (sẽ được bổ sung trong commit tiếp theo)
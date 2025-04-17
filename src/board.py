"""
Chess board representation using logical programming approach
"""

import pygame
from src.constants import BOARD_SIZE, SQUARE_SIZE, LIGHT_SQUARE, DARK_SQUARE, HIGHLIGHT, MOVE_HIGHLIGHT
from src.pieces import get_valid_moves

# Biểu diễn bàn cờ như một tập hợp các facts
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
        'selected_piece': None,
        'valid_moves': []
    }
    return state

def select_piece(game_state, pos):
    """Select a piece at the given position"""
    board = game_state['board']
    piece = board.get(pos, None)
    
    # Clear previous selection
    game_state['selected_piece'] = None
    game_state['valid_moves'] = []
    
    # Check if selected position has a piece of the current player's color
    if piece and piece[1] == game_state['turn']:
        game_state['selected_piece'] = pos
        game_state['valid_moves'] = get_valid_moves(board, game_state, pos)
    
    return game_state

def move_piece(game_state, start_pos, end_pos):
    """Move a piece from start position to end position"""
    board = game_state['board']
    piece = board.get(start_pos, None)
    
    if not piece:
        return game_state
    
    # Check if the move is valid
    valid_moves = get_valid_moves(board, game_state, start_pos)
    if end_pos not in valid_moves:
        return game_state
    
    # Handle special moves
    piece_type, color = piece
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    
    # Create a copy of the current board before making changes
    new_board = dict(board)
    
    # Reset en passant target
    game_state['en_passant_target'] = None
    
    # Check for pawn special moves
    if piece_type == 'P':
        # Check for en passant capture
        if abs(start_col - end_col) == 1 and is_empty(board, end_pos):
            # This must be an en passant move
            capture_pos = (start_row, end_col)  # The position of the captured pawn
            if capture_pos in new_board:
                del new_board[capture_pos]
        
        # Check for promotion (reaching the end rank)
        if (color == 'white' and end_row == 0) or (color == 'black' and end_row == 7):
            # For now, automatically promote to queen
            # In a later commit, we'll add UI for choosing the piece
            new_board[end_pos] = ('Q', color)
        else:
            new_board[end_pos] = piece
            
        # Check for pawn double move (setting en passant target)
        if abs(start_row - end_row) == 2:
            # Set en passant target to the square the pawn skipped
            game_state['en_passant_target'] = (start_row + (1 if color == 'black' else -1), start_col)
    
    # Check for king special moves (castling)
    elif piece_type == 'K':
        # King-side castling
        if start_col + 2 == end_col:
            # Move the king
            new_board[end_pos] = piece
            # Move the rook
            rook_start = (start_row, 7)
            rook_end = (start_row, start_col + 1)
            rook = new_board.get(rook_start)
            if rook:
                new_board[rook_end] = rook
                del new_board[rook_start]
                
        # Queen-side castling
        elif start_col - 2 == end_col:
            # Move the king
            new_board[end_pos] = piece
            # Move the rook
            rook_start = (start_row, 0)
            rook_end = (start_row, start_col - 1)
            rook = new_board.get(rook_start)
            if rook:
                new_board[rook_end] = rook
                del new_board[rook_start]
        else:
            # Normal king move
            new_board[end_pos] = piece
    else:
        # Normal piece move
        new_board[end_pos] = piece
    
    # Remove the piece from its starting position
    if start_pos in new_board:
        del new_board[start_pos]
    
    # Update castling rights
    castling_rights = game_state['castling_rights']
    
    # If king moves, lose all castling rights for that color
    if piece_type == 'K':
        if color == 'white':
            castling_rights['white_king_side'] = False
            castling_rights['white_queen_side'] = False
        else:
            castling_rights['black_king_side'] = False
            castling_rights['black_queen_side'] = False
    
    # If rook moves, lose castling rights for that side
    elif piece_type == 'R':
        if start_pos == (7, 0) and color == 'white':
            castling_rights['white_queen_side'] = False
        elif start_pos == (7, 7) and color == 'white':
            castling_rights['white_king_side'] = False
        elif start_pos == (0, 0) and color == 'black':
            castling_rights['black_queen_side'] = False
        elif start_pos == (0, 7) and color == 'black':
            castling_rights['black_king_side'] = False
    
    # Track king positions
    if piece_type == 'K':
        if color == 'white':
            game_state['white_king_pos'] = end_pos
        else:
            game_state['black_king_pos'] = end_pos
    
    # Update the board
    game_state['board'] = new_board
    
    # Log the move
    game_state['move_history'].append((start_pos, end_pos, piece))
    
    # Switch turns
    game_state['turn'] = 'black' if game_state['turn'] == 'white' else 'white'
    
    # Clear selection
    game_state['selected_piece'] = None
    game_state['valid_moves'] = []
    
    return game_state

def draw_board(screen, game_state):
    """Draw the chess board and pieces"""
    board = game_state['board']
    selected = game_state['selected_piece']
    valid_moves = game_state['valid_moves']
    
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
    
    # Highlight valid moves
    for move in valid_moves:
        row, col = move
        pygame.draw.rect(
            screen,
            MOVE_HIGHLIGHT,
            pygame.Rect(
                col * SQUARE_SIZE,
                row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            )
        )
    
    # Highlight selected piece
    if selected:
        row, col = selected
        pygame.draw.rect(
            screen,
            HIGHLIGHT,
            pygame.Rect(
                col * SQUARE_SIZE,
                row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            )
        )
    
    # Draw pieces placeholder
    for pos, piece in board.items():
        row, col = pos
        piece_type, color = piece
        
        # Simple representation of pieces
        font = pygame.font.SysFont('Arial', 36)
        text_color = (255, 255, 255) if color == 'black' else (0, 0, 0)
        text = font.render(piece_type, True, text_color)
        
        # Center the text in the square
        text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                          row * SQUARE_SIZE + SQUARE_SIZE // 2))
        screen.blit(text, text_rect)
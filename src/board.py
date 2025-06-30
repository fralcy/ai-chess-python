"""
Chess board representation using logical programming approach
"""

import pygame
from src.constants import BOARD_SIZE, SQUARE_SIZE, LIGHT_SQUARE, DARK_SQUARE, HIGHLIGHT, MOVE_HIGHLIGHT, WIDTH
from src.endgame import get_position_key
from src.pieces import is_empty, is_check, is_checkmate, is_stalemate, get_valid_moves_considering_check


# Biểu diễn bàn cờ như một tập hợp các facts
def create_board():
    """Create an initial chess board state as a set of facts"""
    # Format: board[position] = (piece_type, color)
    # position là tuple (row, col)
    # piece_type: 'P' (pawn), 'R' (rook), 'N' (knight), 'B' (bishop), 'Q' (queen), 'K' (king)
    # color: 'white' hoặc 'black'
    
    board = {}
    
    # Tốt trắng sắp phong cấp
    board[(1, 2)] = ('P', 'white')  # Tốt trắng ở hàng 2 (sẽ lên hàng 1)
    
    # Vua (bắt buộc phải có)
    board[(7, 4)] = ('K', 'white')  # Vua trắng
    board[(0, 4)] = ('K', 'black')  # Vua đen
    
    # Thêm ít quân khác
    board[(6, 0)] = ('P', 'white')  # Tốt trắng khác
    board[(1, 0)] = ('P', 'black')  # Tốt đen
    board[(1, 7)] = ('P', 'black')  # Tốt đen
    
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
        'valid_moves': [],
        'halfmove_clock': 0,  # Đếm số nước đi không ăn quân hoặc di chuyển tốt
        'fullmove_number': 1,  # Số lượt đi đầy đủ
        'position_history': []  # Lưu lịch sử các trạng thái bàn cờ để kiểm tra lặp lại
    }
    
    # Lưu trạng thái ban đầu
    state['position_history'].append(get_position_key(state['board']))
    
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
        game_state['valid_moves'] = get_valid_moves_considering_check(board, game_state, pos)
    
    return game_state

def move_piece(game_state, start_pos, end_pos, promotion_piece='Q'):
    """Move a piece from start position to end position with optional promotion piece"""
    board = game_state['board']
    piece = board.get(start_pos, None)
    
    if not piece:
        return game_state
    
    # Check if the move is valid
    valid_moves = get_valid_moves_considering_check(board, game_state, start_pos)
    if end_pos not in valid_moves:
        return game_state
    
    # Handle special moves
    piece_type, color = piece
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    
    # Create a copy of the current board before making changes
    new_board = dict(board)
    
    # QUAN TRỌNG: Xóa en passant target cũ trước khi xử lý nước đi mới
    game_state['en_passant_target'] = None
    
    # Check if this move resets the halfmove clock (capture or pawn move)
    is_capture = end_pos in board  # Destination has an opponent piece
    
    # Cập nhật halfmove_clock
    if piece_type == 'P' or is_capture:
        game_state['halfmove_clock'] = 0  # Reset nếu có ăn quân hoặc di chuyển tốt
    else:
        game_state['halfmove_clock'] += 1  # Tăng nếu không ăn quân và không di chuyển tốt
    
    # Cập nhật fullmove_number sau mỗi lượt của đen
    if color == 'black':
        game_state['fullmove_number'] += 1
    
    # Check for pawn special moves
    if piece_type == 'P':
        # XÓA TỐT Ở VỊ TRÍ CŨ NGAY ĐẦU (quan trọng!)
        if start_pos in new_board:
            del new_board[start_pos]
            
        # Check for en passant capture
        if abs(start_col - end_col) == 1 and is_empty(board, end_pos):
            # This must be an en passant move - xóa tốt bị bắt
            capture_pos = (start_row, end_col)  # The position of the captured pawn
            if capture_pos in new_board:
                del new_board[capture_pos]
        
        # Check for promotion (reaching the end rank)
        if (color == 'white' and end_row == 0) or (color == 'black' and end_row == 7):
            # PROMOTION: Sử dụng promotion_piece parameter
            new_board[end_pos] = (promotion_piece, color)
        else:
            # Normal pawn move (đã xóa tốt cũ ở trên)
            new_board[end_pos] = piece
            
        # FIX: Chỉ đặt en passant target khi tốt đi 2 bước
        if abs(start_row - end_row) == 2:
            # Set en passant target to the square the pawn skipped
            game_state['en_passant_target'] = (start_row + (1 if color == 'black' else -1), start_col)
    
    # Check for castling
    elif piece_type == 'K' and abs(start_col - end_col) == 2:
        # This is a castling move
        # XÓA VUA Ở VỊ TRÍ CŨ TRƯỚC
        if start_pos in new_board:
            del new_board[start_pos]
            
        # Đặt vua ở vị trí mới
        new_board[end_pos] = piece
        
        # Also move the rook
        if end_col > start_col:  # King-side castling
            rook_start = (start_row, 7)
            rook_end = (start_row, 5)
        else:  # Queen-side castling
            rook_start = (start_row, 0)
            rook_end = (start_row, 3)
        
        rook = new_board.get(rook_start)
        if rook:
            new_board[rook_end] = rook
            del new_board[rook_start]
            
        # Update castling rights
        if color == 'white':
            game_state['castling_rights']['white_king_side'] = False
            game_state['castling_rights']['white_queen_side'] = False
        else:
            game_state['castling_rights']['black_king_side'] = False
            game_state['castling_rights']['black_queen_side'] = False
    else:
        # Regular move for all other pieces
        # XÓA QUÂN Ở VỊ TRÍ CŨ TRƯỚC
        if start_pos in new_board:
            del new_board[start_pos]
        # Đặt quân ở vị trí mới
        new_board[end_pos] = piece
        
    # Update castling rights if king or rook moves
    if piece_type == 'K':
        if color == 'white':
            game_state['castling_rights']['white_king_side'] = False
            game_state['castling_rights']['white_queen_side'] = False
            game_state['white_king_pos'] = end_pos
        else:
            game_state['castling_rights']['black_king_side'] = False
            game_state['castling_rights']['black_queen_side'] = False
            game_state['black_king_pos'] = end_pos
    elif piece_type == 'R':
        if color == 'white':
            if start_pos == (7, 0):  # Queen-side rook
                game_state['castling_rights']['white_queen_side'] = False
            elif start_pos == (7, 7):  # King-side rook
                game_state['castling_rights']['white_king_side'] = False
        else:
            if start_pos == (0, 0):  # Queen-side rook
                game_state['castling_rights']['black_queen_side'] = False
            elif start_pos == (0, 7):  # King-side rook
                game_state['castling_rights']['black_king_side'] = False
    
    # Update the board
    game_state['board'] = new_board
    
    # Log the move
    game_state['move_history'].append((start_pos, end_pos, piece))
    
    # Lưu trạng thái mới vào position_history
    from src.endgame import get_position_key
    game_state['position_history'].append(get_position_key(new_board))
    
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
    
    # Check for check, checkmate, or stalemate
    current_color = game_state['turn']
    font = pygame.font.SysFont('Arial', 24)
    
    if is_checkmate(board, game_state, current_color):
        winner = 'Black' if current_color == 'white' else 'White'
        text = font.render(f"{winner} wins by checkmate!", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - 100, 20))
    elif is_stalemate(board, game_state, current_color):
        text = font.render("Game drawn by stalemate!", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - 100, 20))
    elif is_check(board, game_state, current_color):
        text = font.render(f"{current_color.capitalize()} is in check!", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - 100, 20))

def make_hypothetical_move(game_state, start_pos, end_pos):
    """Make a hypothetical move and return the new game state"""
    # Create a copy of the game state
    new_state = {
        'board': dict(game_state['board']),
        'turn': game_state['turn'],
        'white_king_pos': game_state['white_king_pos'],
        'black_king_pos': game_state['black_king_pos'],
        'castling_rights': dict(game_state['castling_rights']),
        'en_passant_target': game_state['en_passant_target'],
        'move_history': list(game_state['move_history']),
        'selected_piece': None,
        'valid_moves': []
    }
    
    # Get the piece
    board = new_state['board']
    piece = board.get(start_pos, None)
    
    if not piece:
        return new_state
    
    piece_type, color = piece
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    
    # Handle special moves like en passant, castling, promotion
    if piece_type == 'P':
        # En passant capture
        if abs(start_col - end_col) == 1 and end_pos not in board:
            # This must be an en passant move
            capture_pos = (start_row, end_col)
            if capture_pos in board:
                del board[capture_pos]
        
        # Promotion (automatically to Queen for now)
        if (color == 'white' and end_row == 0) or (color == 'black' and end_row == 7):
            board[end_pos] = ('Q', color)
        else:
            board[end_pos] = piece
    
    # Castling
    elif piece_type == 'K' and abs(start_col - end_col) == 2:
        board[end_pos] = piece
        
        # Move the rook as well
        if end_col > start_col:  # King-side
            rook_start = (start_row, 7)
            rook_end = (start_row, 5)
        else:  # Queen-side
            rook_start = (start_row, 0)
            rook_end = (start_row, 3)
            
        rook = board.get(rook_start)
        if rook:
            board[rook_end] = rook
            del board[rook_start]
    else:
        # Regular move
        board[end_pos] = piece
    
    # Remove the piece from its starting position if not already done
    if start_pos in board:
        del board[start_pos]
    
    # Update king position if the king moved
    if piece_type == 'K':
        if color == 'white':
            new_state['white_king_pos'] = end_pos
        else:
            new_state['black_king_pos'] = end_pos
    
    # Switch turn
    new_state['turn'] = 'black' if new_state['turn'] == 'white' else 'white'
    
    return new_state
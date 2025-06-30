"""
Chess piece movement rules using logical programming approach
"""

from src.constants import BOARD_SIZE

# Directions vectors
NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)
NORTH_EAST = (-1, 1)
NORTH_WEST = (-1, -1)
SOUTH_EAST = (1, 1)
SOUTH_WEST = (1, -1)

# Knight move patterns
KNIGHT_MOVES = [
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1)
]

def is_valid_position(pos):
    """Check if position is within board boundaries"""
    row, col = pos
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

def get_piece_at(board, pos):
    """Get piece at the given position"""
    return board.get(pos, None)

def is_opponent(piece1, piece2):
    """Check if pieces are opponents"""
    if piece1 is None or piece2 is None:
        return False
    return piece1[1] != piece2[1]

def is_empty(board, pos):
    """Check if a position is empty"""
    return get_piece_at(board, pos) is None

def add_positions(pos1, pos2):
    """Add two positions"""
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])

def get_pawn_moves(board, game_state, pos):
    """Get all valid moves for a pawn at the given position"""
    piece = get_piece_at(board, pos)
    if piece is None or piece[0] != 'P':
        return []
    
    row, col = pos
    moves = []
    
    # Direction depends on color
    direction = -1 if piece[1] == 'white' else 1
    
    # Move forward one step
    next_pos = (row + direction, col)
    if is_valid_position(next_pos) and is_empty(board, next_pos):
        moves.append(next_pos)
        
        # Move forward two steps from starting position
        if (piece[1] == 'white' and row == 6) or (piece[1] == 'black' and row == 1):
            next_pos = (row + 2 * direction, col)
            if is_valid_position(next_pos) and is_empty(board, next_pos):
                moves.append(next_pos)
    
    # Captures
    for dcol in [-1, 1]:
        capture_pos = (row + direction, col + dcol)
        if is_valid_position(capture_pos):
            target = get_piece_at(board, capture_pos)
            if target and is_opponent(piece, target):
                moves.append(capture_pos)
    
    # FIX: En passant với logic đúng
    en_passant_target = game_state.get('en_passant_target')
    if en_passant_target:
        en_row, en_col = en_passant_target
        # Kiểm tra tốt có ở đúng hàng để có thể bắt en passant không
        # Tốt trắng phải ở hàng 3, tốt đen phải ở hàng 4
        if ((piece[1] == 'white' and row == 3) or (piece[1] == 'black' and row == 4)) and \
           abs(col - en_col) == 1:
            # Thêm nước bắt tốt qua đường
            moves.append((row + direction, en_col))
    
    return moves

def get_rook_moves(board, pos):
    """Get all valid moves for a rook at the given position"""
    piece = get_piece_at(board, pos)
    if piece is None or piece[0] != 'R':
        return []
    
    moves = []
    directions = [NORTH, SOUTH, EAST, WEST]
    
    for direction in directions:
        current = pos
        while True:
            current = add_positions(current, direction)
            if not is_valid_position(current):
                break
            
            target = get_piece_at(board, current)
            if target is None:
                moves.append(current)
            elif is_opponent(piece, target):
                moves.append(current)
                break
            else:
                break
    
    return moves

def get_knight_moves(board, pos):
    """Get all valid moves for a knight at the given position"""
    piece = get_piece_at(board, pos)
    if piece is None or piece[0] != 'N':
        return []
    
    moves = []
    
    for offset in KNIGHT_MOVES:
        target_pos = add_positions(pos, offset)
        if is_valid_position(target_pos):
            target = get_piece_at(board, target_pos)
            if target is None or is_opponent(piece, target):
                moves.append(target_pos)
    
    return moves

def get_bishop_moves(board, pos):
    """Get all valid moves for a bishop at the given position"""
    piece = get_piece_at(board, pos)
    if piece is None or piece[0] != 'B':
        return []
    
    moves = []
    directions = [NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST]
    
    for direction in directions:
        current = pos
        while True:
            current = add_positions(current, direction)
            if not is_valid_position(current):
                break
            
            target = get_piece_at(board, current)
            if target is None:
                moves.append(current)
            elif is_opponent(piece, target):
                moves.append(current)
                break
            else:
                break
    
    return moves

def get_queen_moves(board, pos):
    """Get all valid moves for a queen at the given position"""
    piece = get_piece_at(board, pos)
    if piece is None or piece[0] != 'Q':
        return []
    
    # Queen combines rook and bishop moves
    moves = []
    directions = [NORTH, SOUTH, EAST, WEST, NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST]
    
    for direction in directions:
        current = pos
        while True:
            current = add_positions(current, direction)
            if not is_valid_position(current):
                break
            
            target = get_piece_at(board, current)
            if target is None:
                moves.append(current)
            elif is_opponent(piece, target):
                moves.append(current)
                break
            else:
                break
    
    return moves

def get_king_moves(board, game_state, pos):
    """Get all valid moves for a king at the given position"""
    piece = get_piece_at(board, pos)
    if piece is None or piece[0] != 'K':
        return []
    
    moves = []
    directions = [NORTH, SOUTH, EAST, WEST, NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST]
    
    for direction in directions:
        target_pos = add_positions(pos, direction)
        if is_valid_position(target_pos):
            target = get_piece_at(board, target_pos)
            if target is None or is_opponent(piece, target):
                moves.append(target_pos)
    
    # Castling
    castling_rights = game_state['castling_rights']
    row = pos[0]
    col = pos[1]
    color = piece[1]
    opponent_color = 'black' if color == 'white' else 'white'
    
    # Chỉ kiểm tra nhập thành nếu được truyền vào đầy đủ thông tin
    if 'castling_rights' in game_state and 'en_passant_target' in game_state:
        # Kiểm tra xem Vua có đang bị chiếu không
        # Sử dụng một phiên bản đơn giản hơn của is_square_under_attack để tránh đệ quy vô tận
        if not is_king_in_check_simple(board, pos, opponent_color):
            # Function to check if squares between king and rook are empty and not under attack
            def squares_clear_and_safe(start_col, end_col):
                for c in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                    if get_piece_at(board, (row, c)) is not None:
                        return False
                    
                    # Kiểm tra các ô mà Vua đi qua có bị tấn công không
                    if not is_king_in_check_simple(board, (row, c), opponent_color):
                        continue
                    else:
                        return False
                        
                return True
            
            # Check for castling conditions
            if color == 'white':
                # King-side castling
                if castling_rights['white_king_side'] and squares_clear_and_safe(col, 7):
                    if get_piece_at(board, (row, 7)) == ('R', 'white'):
                        moves.append((row, col + 2))  # King's target position
                        
                # Queen-side castling
                if castling_rights['white_queen_side'] and squares_clear_and_safe(col, 0):
                    if get_piece_at(board, (row, 0)) == ('R', 'white'):
                        moves.append((row, col - 2))  # King's target position
            else:
                # King-side castling
                if castling_rights['black_king_side'] and squares_clear_and_safe(col, 7):
                    if get_piece_at(board, (row, 7)) == ('R', 'black'):
                        moves.append((row, col + 2))  # King's target position
                        
                # Queen-side castling
                if castling_rights['black_queen_side'] and squares_clear_and_safe(col, 0):
                    if get_piece_at(board, (row, 0)) == ('R', 'black'):
                        moves.append((row, col - 2))  # King's target position
    
    return moves

def is_king_in_check_simple(board, king_pos, attacking_color):
    """
    Phiên bản đơn giản hơn của is_square_under_attack
    Kiểm tra xem vua có đang bị chiếu không mà không gọi đệ quy vào get_king_moves
    """
    # Kiểm tra tấn công từ các hướng Xe/Hậu (ngang, dọc)
    for direction in [NORTH, SOUTH, EAST, WEST]:
        current = king_pos
        while True:
            current = add_positions(current, direction)
            if not is_valid_position(current):
                break
                
            piece = get_piece_at(board, current)
            if piece is None:
                continue
                
            piece_type, color = piece
            if color == attacking_color and (piece_type == 'R' or piece_type == 'Q'):
                return True
            else:
                break
    
    # Kiểm tra tấn công từ các hướng Tượng/Hậu (chéo)
    for direction in [NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST]:
        current = king_pos
        while True:
            current = add_positions(current, direction)
            if not is_valid_position(current):
                break
                
            piece = get_piece_at(board, current)
            if piece is None:
                continue
                
            piece_type, color = piece
            if color == attacking_color and (piece_type == 'B' or piece_type == 'Q'):
                return True
            else:
                break
    
    # Kiểm tra tấn công từ Mã
    for offset in KNIGHT_MOVES:
        current = add_positions(king_pos, offset)
        if not is_valid_position(current):
            continue
            
        piece = get_piece_at(board, current)
        if piece is not None:
            piece_type, color = piece
            if color == attacking_color and piece_type == 'N':
                return True
    
    # Kiểm tra tấn công từ Tốt
    row, col = king_pos
    pawn_row_offset = 1 if attacking_color == 'white' else -1
    for c_offset in [-1, 1]:
        pawn_pos = (row + pawn_row_offset, col + c_offset)
        if not is_valid_position(pawn_pos):
            continue
            
        piece = get_piece_at(board, pawn_pos)
        if piece is not None:
            piece_type, color = piece
            if color == attacking_color and piece_type == 'P':
                return True
    
    # Kiểm tra tấn công từ Vua đối phương (cho các trường hợp đặc biệt)
    for direction in [NORTH, SOUTH, EAST, WEST, NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST]:
        current = add_positions(king_pos, direction)
        if not is_valid_position(current):
            continue
            
        piece = get_piece_at(board, current)
        if piece is not None:
            piece_type, color = piece
            if color == attacking_color and piece_type == 'K':
                return True
    
    return False

def get_valid_moves(board, game_state, pos):
    """Get all valid moves for a piece at the given position"""
    piece = get_piece_at(board, pos)
    if piece is None:
        return []
    
    piece_type = piece[0]
    
    if piece_type == 'P':
        return get_pawn_moves(board, game_state, pos)
    elif piece_type == 'R':
        return get_rook_moves(board, pos)
    elif piece_type == 'N':
        return get_knight_moves(board, pos)
    elif piece_type == 'B':
        return get_bishop_moves(board, pos)
    elif piece_type == 'Q':
        return get_queen_moves(board, pos)
    elif piece_type == 'K':
        return get_king_moves(board, game_state, pos)
    
    return []

def is_square_under_attack(board, game_state, square, attacking_color):
    """Check if a square is under attack by a piece of the given color"""
    row, col = square
    
    # Kiểm tra vị trí của vua để tránh đệ quy vô tận
    king_pos = game_state.get('white_king_pos' if attacking_color == 'black' else 'black_king_pos')
    if square == king_pos:
        return is_king_in_check_simple(board, square, attacking_color)
    
    for pos, piece in board.items():
        piece_type, color = piece
        if color == attacking_color:
            # Get valid moves for this piece
            moves = []
            if piece_type == 'P':
                # Special case for pawns - they can attack diagonally
                p_row, p_col = pos
                direction = -1 if color == 'white' else 1
                attacks = [(p_row + direction, p_col - 1), (p_row + direction, p_col + 1)]
                moves = [attack for attack in attacks if is_valid_position(attack)]
            else:
                # For other pieces, use the normal move generation
                # But pass a simplified game state (to avoid recursion)
                simple_state = {'castling_rights': game_state['castling_rights'],
                               'en_passant_target': game_state['en_passant_target']}
                if piece_type == 'K':
                    # For king, just use basic moves without castling
                    moves = []
                    king_row, king_col = pos
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            target = (king_row + dr, king_col + dc)
                            if is_valid_position(target):
                                target_piece = get_piece_at(board, target)
                                if target_piece is None or is_opponent(piece, target_piece):
                                    moves.append(target)
                elif piece_type == 'Q':
                    moves = get_queen_moves(board, pos)
                elif piece_type == 'R':
                    moves = get_rook_moves(board, pos)
                elif piece_type == 'B':
                    moves = get_bishop_moves(board, pos)
                elif piece_type == 'N':
                    moves = get_knight_moves(board, pos)
            
            # Check if the square is in the valid moves
            if square in moves:
                return True
    
    return False

def is_check(board, game_state, color):
    """Check if the king of the given color is in check"""
    # Get king position
    king_pos = game_state['white_king_pos'] if color == 'white' else game_state['black_king_pos']
    
    # Check if the king is under attack
    opponent_color = 'black' if color == 'white' else 'white'
    return is_square_under_attack(board, game_state, king_pos, opponent_color)

def is_checkmate(board, game_state, color):
    """Check if the king of the given color is in checkmate"""
    # First, check if the king is in check
    if not is_check(board, game_state, color):
        return False
    
    # Check if any move can get the king out of check
    for pos, piece in board.items():
        piece_type, piece_color = piece
        if piece_color == color:
            valid_moves = get_valid_moves(board, game_state, pos)
            for move in valid_moves:
                # Make a hypothetical move
                new_state = make_hypothetical_move(game_state, pos, move)
                # Check if this move gets out of check
                if not is_check(new_state['board'], new_state, color):
                    return False
    
    # If no move can get the king out of check, it's checkmate
    return True

def is_stalemate(board, game_state, color):
    """Check if the position is a stalemate for the given color"""
    # First, check if the king is NOT in check
    if is_check(board, game_state, color):
        return False
    
    # Check if any valid move exists
    for pos, piece in board.items():
        piece_type, piece_color = piece
        if piece_color == color:
            valid_moves = get_valid_moves(board, game_state, pos)
            for move in valid_moves:
                # Make a hypothetical move
                new_state = make_hypothetical_move(game_state, pos, move)
                # Check if this move doesn't put the king in check
                if not is_check(new_state['board'], new_state, color):
                    return False
    
    # If no legal move exists, it's stalemate
    return True

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
            # Remove pawn from its starting position
            if start_pos in board:
                del board[start_pos]
        else:
            board[end_pos] = piece
            if start_pos in board:
                del board[start_pos]
    
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
        if start_pos in board:
            del board[start_pos]
    else:
        # Regular move
        board[end_pos] = piece
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

def get_valid_moves_considering_check(board, game_state, pos):
    """Get all valid moves for a piece, considering check rules"""
    piece = get_piece_at(board, pos)
    if piece is None:
        return []
    
    color = piece[1]
    
    # Get all possible moves without considering check
    all_moves = get_valid_moves(board, game_state, pos)
    legal_moves = []
    
    # Test each move to see if it leaves the king in check
    for move in all_moves:
        # Make a hypothetical move
        new_state = make_hypothetical_move(game_state, pos, move)
        # Check if this move leaves the king in check
        if not is_check(new_state['board'], new_state, color):
            legal_moves.append(move)
    
    return legal_moves
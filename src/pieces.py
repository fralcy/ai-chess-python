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
    
    # En passant
    en_passant_target = game_state.get('en_passant_target')
    if en_passant_target:
        en_row, en_col = en_passant_target
        # Check if our pawn is in the right position to capture en passant
        if (row == en_row and abs(col - en_col) == 1 and 
            ((piece[1] == 'white' and row == 3) or (piece[1] == 'black' and row == 4))):
            moves.append((row + direction, en_col))
    
    # Note: Promotion is handled in the move_piece function
    # when a pawn reaches the last rank
    
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
    
    # Kiểm tra xem Vua có đang bị chiếu không
    if is_square_under_attack(board, game_state, pos, opponent_color):
        return moves  # Nếu đang bị chiếu, không thể nhập thành
    
    # Function to check if squares between king and rook are empty and not under attack
    def squares_clear_and_safe(start_col, end_col):
        for c in range(min(start_col, end_col) + 1, max(start_col, end_col)):
            if get_piece_at(board, (row, c)) is not None:
                return False
            
            # Kiểm tra các ô mà Vua đi qua có bị tấn công không
            if c != end_col and is_square_under_attack(board, game_state, (row, c), opponent_color):
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
    for pos, piece in board.items():
        piece_type, color = piece
        if color == attacking_color:
            # Get valid moves for this piece
            moves = []
            if piece_type == 'P':
                # Special case for pawns - they can attack diagonally
                row, col = pos
                direction = -1 if color == 'white' else 1
                attacks = [(row + direction, col - 1), (row + direction, col + 1)]
                moves = [attack for attack in attacks if is_valid_position(attack)]
            else:
                # For other pieces, use the normal move generation
                # But pass a simplified game state (to avoid recursion)
                simple_state = {'castling_rights': game_state['castling_rights'],
                               'en_passant_target': game_state['en_passant_target']}
                if piece_type == 'K':
                    moves = get_king_moves(board, simple_state, pos)
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
    
    # Move the piece
    board[end_pos] = piece
    del board[start_pos]
    
    # Update king position if the king moved
    if piece[0] == 'K':
        if piece[1] == 'white':
            new_state['white_king_pos'] = end_pos
        else:
            new_state['black_king_pos'] = end_pos
    
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
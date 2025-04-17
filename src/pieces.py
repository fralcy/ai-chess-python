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

def get_pawn_moves(board, pos):
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
    
    # En passant will be added in the next commit
    
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

def get_king_moves(board, pos):
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
    
    # Castling will be added in a future commit
    
    return moves

def get_valid_moves(board, pos):
    """Get all valid moves for a piece at the given position"""
    piece = get_piece_at(board, pos)
    if piece is None:
        return []
    
    piece_type = piece[0]
    
    if piece_type == 'P':
        return get_pawn_moves(board, pos)
    elif piece_type == 'R':
        return get_rook_moves(board, pos)
    elif piece_type == 'N':
        return get_knight_moves(board, pos)
    elif piece_type == 'B':
        return get_bishop_moves(board, pos)
    elif piece_type == 'Q':
        return get_queen_moves(board, pos)
    elif piece_type == 'K':
        return get_king_moves(board, pos)
    
    return []
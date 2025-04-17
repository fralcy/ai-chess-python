"""
Endgame rules and detection
"""

def get_position_key(board):
    """
    Tạo khóa duy nhất cho trạng thái bàn cờ hiện tại
    Sử dụng để kiểm tra trùng lặp vị trí (Threefold Repetition)
    """
    # Sắp xếp các vị trí quân cờ để tạo khóa nhất quán
    pieces = []
    for pos, piece in sorted(board.items()):
        pieces.append(f"{pos}:{piece[0]}{piece[1][0]}")  # Ví dụ: (0,0):Rb (Xe đen ở 0,0)
    
    return ":".join(pieces)

def is_insufficient_material(board):
    """
    Kiểm tra xem có đủ quân mạnh để chiếu hết không
    Các trường hợp không đủ quân mạnh:
    - Vua vs Vua
    - Vua vs Vua + Mã
    - Vua vs Vua + Tượng
    - Vua + Tượng vs Vua + Tượng (cùng màu ô)
    """
    # Đếm số quân và loại quân
    white_pieces = {'K': 0, 'Q': 0, 'R': 0, 'B': 0, 'N': 0, 'P': 0}
    black_pieces = {'K': 0, 'Q': 0, 'R': 0, 'B': 0, 'N': 0, 'P': 0}
    white_bishop_square_color = None
    black_bishop_square_color = None
    
    for pos, piece in board.items():
        piece_type, color = piece
        row, col = pos
        
        if color == 'white':
            white_pieces[piece_type] += 1
            # Lưu màu ô của Tượng trắng (đen/trắng)
            if piece_type == 'B' and white_bishop_square_color is None:
                white_bishop_square_color = (row + col) % 2
        else:
            black_pieces[piece_type] += 1
            # Lưu màu ô của Tượng đen
            if piece_type == 'B' and black_bishop_square_color is None:
                black_bishop_square_color = (row + col) % 2
    
    # Xóa Vua ra khỏi danh sách để dễ đếm
    white_pieces['K'] -= 1
    black_pieces['K'] -= 1
    
    # Tính tổng quân của mỗi bên (trừ Vua)
    white_total = sum(white_pieces.values())
    black_total = sum(black_pieces.values())
    
    # Trường hợp 1: Vua vs Vua
    if white_total == 0 and black_total == 0:
        return True
    
    # Trường hợp 2: Vua vs Vua + Mã
    if (white_total == 0 and black_total == 1 and black_pieces['N'] == 1) or \
       (black_total == 0 and white_total == 1 and white_pieces['N'] == 1):
        return True
    
    # Trường hợp 3: Vua vs Vua + Tượng
    if (white_total == 0 and black_total == 1 and black_pieces['B'] == 1) or \
       (black_total == 0 and white_total == 1 and white_pieces['B'] == 1):
        return True
    
    # Trường hợp 4: Vua + Tượng vs Vua + Tượng (cùng màu ô)
    if white_total == 1 and black_total == 1 and \
       white_pieces['B'] == 1 and black_pieces['B'] == 1 and \
       white_bishop_square_color == black_bishop_square_color:
        return True
    
    return False

def is_threefold_repetition(game_state):
    """
    Kiểm tra xem vị trí hiện tại đã xuất hiện 3 lần chưa
    """
    current_position = get_position_key(game_state['board'])
    return game_state['position_history'].count(current_position) >= 3

def is_fifty_move_rule(game_state):
    """
    Kiểm tra xem đã đủ 50 nước không ăn quân hoặc di chuyển tốt chưa
    """
    return game_state['halfmove_clock'] >= 100  # 50 lượt * 2 nửa lượt = 100
"""
Chess AI using Minimax algorithm with Alpha-Beta pruning
"""

from src.pieces import get_valid_moves_considering_check, is_check, is_checkmate
from src.board import make_hypothetical_move

# Giá trị của từng loại quân cờ
PIECE_VALUES = {
    'P': 10,   # Tốt
    'N': 30,   # Mã
    'B': 30,   # Tượng
    'R': 50,   # Xe
    'Q': 90,   # Hậu
    'K': 900   # Vua
}

# Bảng giá trị vị trí cho các quân cờ
# Tốt sẽ được thêm điểm khi tiến gần đến cuối bàn cờ
PAWN_POSITION_VALUE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

# Mã được ưu tiên ở vị trí trung tâm
KNIGHT_POSITION_VALUE = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

def evaluate_board(board, game_state):
    """
    Đánh giá trạng thái bàn cờ.
    Giá trị dương có lợi cho bên trắng, giá trị âm có lợi cho bên đen.
    """
    if not board:  # Bảo vệ trường hợp bàn cờ rỗng (không nên xảy ra)
        return 0
        
    # Kiểm tra chiếu hết
    if is_checkmate(board, game_state, 'white'):
        return -10000  # Đen thắng
    if is_checkmate(board, game_state, 'black'):
        return 10000  # Trắng thắng
    
    total_eval = 0
    
    for pos, piece in board.items():
        row, col = pos
        piece_type, color = piece
        piece_value = PIECE_VALUES[piece_type]
        
        # Thêm giá trị vị trí
        position_value = 0
        if piece_type == 'P':
            # Đảo ngược bảng giá trị cho quân đen
            if color == 'white':
                position_value = PAWN_POSITION_VALUE[row][col]
            else:
                position_value = PAWN_POSITION_VALUE[7-row][col]
        elif piece_type == 'N':
            # Đảo ngược bảng giá trị cho quân đen
            if color == 'white':
                position_value = KNIGHT_POSITION_VALUE[row][col]
            else:
                position_value = KNIGHT_POSITION_VALUE[7-row][col]
        
        # Tổng giá trị = giá trị cơ bản + giá trị vị trí
        piece_total_value = piece_value + position_value * 0.1
        
        # Nếu là quân đen, giá trị âm
        if color == 'black':
            piece_total_value = -piece_total_value
            
        total_eval += piece_total_value
    
    # Kiểm tra chiếu
    if is_check(board, game_state, 'white'):
        total_eval -= 50  # Trừ điểm nếu trắng bị chiếu
    if is_check(board, game_state, 'black'):
        total_eval += 50  # Cộng điểm nếu đen bị chiếu
    
    return total_eval

def minimax_alpha_beta(game_state, depth, alpha, beta, maximizing_player):
    """
    Thuật toán Minimax với cắt tỉa Alpha-Beta
    game_state: trạng thái hiện tại của bàn cờ
    depth: độ sâu tìm kiếm
    alpha, beta: tham số cắt tỉa Alpha-Beta
    maximizing_player: True nếu người chơi đang tối đa hóa (bên trắng), False nếu đang tối thiểu hóa (bên đen)
    """
    # Trường hợp cơ bản: đạt độ sâu 0 hoặc kết thúc ván đấu
    if depth == 0:
        return evaluate_board(game_state['board'], game_state)
    
    board = game_state['board']
    current_color = 'white' if maximizing_player else 'black'
    
    # Tìm tất cả các nước đi hợp lệ cho quân của người chơi hiện tại
    possible_moves = []
    for pos, piece in board.items():
        piece_type, color = piece
        if color == current_color:
            valid_moves = get_valid_moves_considering_check(board, game_state, pos)
            for move in valid_moves:
                possible_moves.append((pos, move))
    
    # Nếu không có nước đi nào, có thể là chiếu hết hoặc hòa cờ
    if not possible_moves:
        # Kiểm tra trong hàm đánh giá
        return evaluate_board(game_state['board'], game_state)
    
    if maximizing_player:
        max_eval = float('-inf')
        for start, end in possible_moves:
            # Thực hiện nước đi thử nghiệm
            new_state = make_hypothetical_move(game_state, start, end)
            # Đệ quy Minimax với độ sâu giảm 1
            eval = minimax_alpha_beta(new_state, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Cắt tỉa Beta
        return max_eval
    else:
        min_eval = float('inf')
        for start, end in possible_moves:
            # Thực hiện nước đi thử nghiệm
            new_state = make_hypothetical_move(game_state, start, end)
            # Đệ quy Minimax với độ sâu giảm 1
            eval = minimax_alpha_beta(new_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Cắt tỉa Alpha
        return min_eval

def order_moves(game_state, moves):
    """
    Sắp xếp các nước đi để tối ưu cắt tỉa Alpha-Beta.
    Các nước đi có khả năng tốt hơn được xét trước.
    """
    board = game_state['board']
    move_scores = []
    
    for start, end in moves:
        score = 0
        piece = board.get(start)
        if not piece:
            continue
            
        piece_type, color = piece
        
        # Ưu tiên nước bắt quân
        capture = board.get(end)
        if capture:
            capture_type, _ = capture
            score = 10 * PIECE_VALUES[capture_type] - PIECE_VALUES[piece_type]
        
        # Ưu tiên phong cấp tốt
        if piece_type == 'P':
            end_row = end[0]
            if (color == 'white' and end_row == 0) or (color == 'black' and end_row == 7):
                score += 900  # Giá trị của hậu
        
        move_scores.append((score, (start, end)))
    
    # Sắp xếp giảm dần theo điểm số
    move_scores.sort(reverse=True, key=lambda x: x[0])
    return [move for _, move in move_scores]

def find_best_move(game_state, depth=3):
    """
    Tìm nước đi tốt nhất cho AI sử dụng Minimax với cắt tỉa Alpha-Beta
    """
    board = game_state['board']
    current_color = game_state['turn']
    maximizing_player = (current_color == 'white')
    
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    
    if maximizing_player:
        best_value = float('-inf')
    else:
        best_value = float('inf')
    
    # Tìm tất cả các nước đi hợp lệ
    possible_moves = []
    for pos, piece in board.items():
        piece_type, color = piece
        if color == current_color:
            valid_moves = get_valid_moves_considering_check(board, game_state, pos)
            for move in valid_moves:
                possible_moves.append((pos, move))
    
    # Sắp xếp nước đi để tối ưu cắt tỉa
    possible_moves = order_moves(game_state, possible_moves)
    
    # Đánh giá từng nước đi
    for start, end in possible_moves:
        # Thực hiện nước đi thử nghiệm
        new_state = make_hypothetical_move(game_state, start, end)
        # Tính giá trị bằng Minimax với Alpha-Beta
        value = minimax_alpha_beta(new_state, depth - 1, alpha, beta, not maximizing_player)
        
        # Cập nhật nước đi tốt nhất
        if maximizing_player and value > best_value:
            best_value = value
            best_move = (start, end)
            alpha = max(alpha, best_value)
        elif not maximizing_player and value < best_value:
            best_value = value
            best_move = (start, end)
            beta = min(beta, best_value)
    
    return best_move
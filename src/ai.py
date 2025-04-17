"""
Chess AI using Minimax algorithm with Alpha-Beta pruning
"""

import time
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

# Cache lưu trữ kết quả đánh giá trạng thái bàn cờ
evaluation_cache = {}

# Cache lưu trữ các nước đi hợp lệ
valid_moves_cache = {}

def get_board_key(board):
    """Tạo khóa duy nhất cho bàn cờ để dùng trong cache"""
    pieces = []
    for pos, piece in sorted(board.items()):
        pieces.append(f"{pos}:{piece[0]}{piece[1][0]}")
    return ":".join(pieces)

def get_state_key(game_state):
    """Tạo khóa duy nhất cho trạng thái để dùng trong cache"""
    board_key = get_board_key(game_state['board'])
    castling = "-".join([f"{k}:{v}" for k, v in sorted(game_state['castling_rights'].items())])
    en_passant = str(game_state['en_passant_target'])
    turn = game_state['turn']
    return f"{board_key}|{turn}|{castling}|{en_passant}"

def evaluate_board(board, game_state):
    """
    Đánh giá trạng thái bàn cờ.
    Giá trị dương có lợi cho bên trắng, giá trị âm có lợi cho bên đen.
    """
    # Kiểm tra cache trước
    board_key = get_board_key(board)
    if board_key in evaluation_cache:
        return evaluation_cache[board_key]
        
    if not board:  # Bảo vệ trường hợp bàn cờ rỗng (không nên xảy ra)
        return 0
        
    # Kiểm tra chiếu hết
    if is_checkmate(board, game_state, 'white'):
        return -10000  # Đen thắng
    if is_checkmate(board, game_state, 'black'):
        return 10000  # Trắng thắng
    
    total_eval = 0
    
    # Số quân trên bàn cờ
    white_material = 0
    black_material = 0
    
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
        
        # Cập nhật tổng giá trị quân
        if color == 'white':
            white_material += piece_value
            total_eval += piece_total_value
        else:
            black_material += piece_value
            total_eval -= piece_total_value
    
    # Bổ sung: Thưởng cho giai đoạn tàn cuộc khi có lợi thế vật chất
    # Khuyến khích AI trao đổi quân khi đang có lợi thế
    if white_material > black_material and white_material < 30:
        total_eval += (30 - black_material) * 0.5
    elif black_material > white_material and black_material < 30:
        total_eval -= (30 - white_material) * 0.5
    
    # Kiểm tra chiếu
    if is_check(board, game_state, 'white'):
        total_eval -= 50  # Trừ điểm nếu trắng bị chiếu
    if is_check(board, game_state, 'black'):
        total_eval += 50  # Cộng điểm nếu đen bị chiếu
    
    # Lưu kết quả vào cache
    evaluation_cache[board_key] = total_eval
    
    return total_eval

def get_all_valid_moves(board, game_state, color):
    """Lấy tất cả các nước đi hợp lệ cho một bên"""
    # Kiểm tra cache trước
    state_key = get_state_key(game_state) + f"|{color}"
    if state_key in valid_moves_cache:
        return valid_moves_cache[state_key]
    
    moves = []
    for pos, piece in board.items():
        piece_type, piece_color = piece
        if piece_color == color:
            valid_moves = get_valid_moves_considering_check(board, game_state, pos)
            for move in valid_moves:
                moves.append((pos, move))
    
    # Lưu vào cache
    valid_moves_cache[state_key] = moves
    
    return moves

def minimax_alpha_beta(game_state, depth, alpha, beta, maximizing_player, max_time, start_time):
    """
    Thuật toán Minimax với cắt tỉa Alpha-Beta và giới hạn thời gian
    """
    # Kiểm tra thời gian
    if time.time() - start_time > max_time:
        # Nếu đã vượt quá thời gian, trả về giá trị hiện tại
        return evaluate_board(game_state['board'], game_state)
    
    # Trường hợp cơ bản: đạt độ sâu 0 hoặc kết thúc ván đấu
    if depth == 0:
        return evaluate_board(game_state['board'], game_state)
    
    board = game_state['board']
    current_color = 'white' if maximizing_player else 'black'
    
    # Tìm tất cả các nước đi hợp lệ cho quân của người chơi hiện tại
    possible_moves = get_all_valid_moves(board, game_state, current_color)
    
    # Nếu không có nước đi nào, có thể là chiếu hết hoặc hòa cờ
    if not possible_moves:
        # Kiểm tra trong hàm đánh giá
        return evaluate_board(game_state['board'], game_state)
    
    # Sắp xếp nước đi để tối ưu cắt tỉa
    possible_moves = order_moves(game_state, possible_moves)
    
    if maximizing_player:
        max_eval = float('-inf')
        for start, end in possible_moves:
            # Thực hiện nước đi thử nghiệm
            new_state = make_hypothetical_move(game_state, start, end)
            # Đệ quy Minimax với độ sâu giảm 1
            eval = minimax_alpha_beta(new_state, depth - 1, alpha, beta, False, max_time, start_time)
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
            eval = minimax_alpha_beta(new_state, depth - 1, alpha, beta, True, max_time, start_time)
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
        
        # Ưu tiên di chuyển vào trung tâm bàn cờ trong giai đoạn đầu
        center_distance = abs(end[0] - 3.5) + abs(end[1] - 3.5)
        score -= center_distance * 2
        
        move_scores.append((score, (start, end)))
    
    # Sắp xếp giảm dần theo điểm số
    move_scores.sort(reverse=True, key=lambda x: x[0])
    return [move for _, move in move_scores]

def find_best_move(game_state, depth=3):
    """
    Tìm nước đi tốt nhất cho AI sử dụng Minimax với cắt tỉa Alpha-Beta
    """
    # Xóa cache khi bắt đầu tính toán mới
    if len(evaluation_cache) > 10000:
        evaluation_cache.clear()
    if len(valid_moves_cache) > 10000:
        valid_moves_cache.clear()
    
    # Thiết lập thời gian tối đa cho mỗi nước đi dựa vào độ khó
    max_time = 1.0  # 1 giây cho độ khó dễ
    if depth == 3:
        max_time = 2.0  # 2 giây cho độ khó trung bình
    elif depth == 4:
        max_time = 3.0  # 3 giây cho độ khó khó
    
    start_time = time.time()
    
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
    possible_moves = get_all_valid_moves(board, game_state, current_color)
    
    # Sắp xếp nước đi để tối ưu cắt tỉa
    possible_moves = order_moves(game_state, possible_moves)
    
    # Thử Iterative Deepening - tăng dần độ sâu
    current_depth = 1
    iterative_best_move = None
    
    while current_depth <= depth and time.time() - start_time < max_time * 0.8:
        temp_best_value = float('-inf') if maximizing_player else float('inf')
        temp_best_move = None
        
        # Đánh giá từng nước đi
        for start, end in possible_moves:
            # Thực hiện nước đi thử nghiệm
            new_state = make_hypothetical_move(game_state, start, end)
            # Tính giá trị bằng Minimax với Alpha-Beta
            value = minimax_alpha_beta(new_state, current_depth - 1, alpha, beta, not maximizing_player, max_time, start_time)
            
            # Cập nhật nước đi tốt nhất
            if maximizing_player and value > temp_best_value:
                temp_best_value = value
                temp_best_move = (start, end)
                alpha = max(alpha, temp_best_value)
            elif not maximizing_player and value < temp_best_value:
                temp_best_value = value
                temp_best_move = (start, end)
                beta = min(beta, temp_best_value)
                
            # Kiểm tra thời gian sau mỗi nước đi
            if time.time() - start_time > max_time * 0.9:
                break
        
        # Lưu kết quả của độ sâu hiện tại
        if temp_best_move:
            iterative_best_move = temp_best_move
            best_value = temp_best_value
        
        # Tăng độ sâu cho lần lặp tiếp theo
        current_depth += 1
        
        # Nếu gần hết thời gian, thoát vòng lặp
        if time.time() - start_time > max_time * 0.8:
            break
    
    # Nếu đã tìm được nước đi tốt nhất trong Iterative Deepening
    if iterative_best_move:
        return iterative_best_move
    
    # Nếu không có kết quả từ Iterative Deepening (hiếm khi xảy ra), thì xử lý như trước
    for start, end in possible_moves:
        # Thực hiện nước đi thử nghiệm
        new_state = make_hypothetical_move(game_state, start, end)
        # Tính giá trị bằng Minimax với Alpha-Beta
        value = minimax_alpha_beta(new_state, depth - 1, alpha, beta, not maximizing_player, max_time, start_time)
        
        # Cập nhật nước đi tốt nhất
        if maximizing_player and value > best_value:
            best_value = value
            best_move = (start, end)
            alpha = max(alpha, best_value)
        elif not maximizing_player and value < best_value:
            best_value = value
            best_move = (start, end)
            beta = min(beta, best_value)
    
    # Nếu không tìm được nước đi (hiếm khi xảy ra), chọn nước đầu tiên
    if not best_move and possible_moves:
        best_move = possible_moves[0]
    
    return best_move
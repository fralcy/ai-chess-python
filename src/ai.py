"""
Chess AI using Minimax algorithm
"""

from src.pieces import get_valid_moves_considering_check
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

def evaluate_board(board):
    """
    Đánh giá trạng thái bàn cờ.
    Giá trị dương có lợi cho bên trắng, giá trị âm có lợi cho bên đen.
    """
    total_eval = 0
    
    for pos, piece in board.items():
        piece_type, color = piece
        piece_value = PIECE_VALUES[piece_type]
        
        # Nếu là quân đen, giá trị âm
        if color == 'black':
            piece_value = -piece_value
            
        total_eval += piece_value
    
    return total_eval

def minimax(game_state, depth, maximizing_player):
    """
    Thuật toán Minimax cơ bản
    game_state: trạng thái hiện tại của bàn cờ
    depth: độ sâu tìm kiếm
    maximizing_player: True nếu người chơi đang tối đa hóa (bên trắng), False nếu đang tối thiểu hóa (bên đen)
    """
    # Trường hợp cơ bản: đạt độ sâu 0
    if depth == 0:
        return evaluate_board(game_state['board'])
    
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
    
    # Nếu không có nước đi nào, trả về giá trị đánh giá hiện tại
    if not possible_moves:
        return evaluate_board(game_state['board'])
    
    if maximizing_player:
        max_eval = float('-inf')
        for start, end in possible_moves:
            # Thực hiện nước đi thử nghiệm
            new_state = make_hypothetical_move(game_state, start, end)
            # Đệ quy Minimax với độ sâu giảm 1
            eval = minimax(new_state, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for start, end in possible_moves:
            # Thực hiện nước đi thử nghiệm
            new_state = make_hypothetical_move(game_state, start, end)
            # Đệ quy Minimax với độ sâu giảm 1
            eval = minimax(new_state, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def find_best_move(game_state, depth=3):
    """
    Tìm nước đi tốt nhất cho AI
    """
    board = game_state['board']
    current_color = game_state['turn']
    maximizing_player = (current_color == 'white')
    
    best_move = None
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
    
    # Đánh giá từng nước đi
    for start, end in possible_moves:
        # Thực hiện nước đi thử nghiệm
        new_state = make_hypothetical_move(game_state, start, end)
        # Tính giá trị bằng Minimax
        value = minimax(new_state, depth - 1, not maximizing_player)
        
        # Cập nhật nước đi tốt nhất
        if maximizing_player and value > best_value:
            best_value = value
            best_move = (start, end)
        elif not maximizing_player and value < best_value:
            best_value = value
            best_move = (start, end)
    
    return best_move
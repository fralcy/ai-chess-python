import sys
from logic.game_state import GameState
from logic.player import Player
from ai.evaluator import BoardEvaluator

def minimax(game_state: GameState, depth, maximizing_player: Player):
    """
    Basic minimax algorithm without optimizations.
    
    Args:
        game_state: The current game state
        depth: How many moves ahead to look
        maximizing_player: The player that is maximizing the score
    
    Returns:
        The best score achievable and the best move to make
    """
    # Base case: reached depth limit or game over
    if depth == 0 or game_state.is_game_over():
        # Return the evaluation score from the perspective of maximizing player
        score = BoardEvaluator.evaluate(game_state.board, maximizing_player)
        return score, None
    
    # Get legal moves for current player
    legal_moves = game_state.all_legal_moves_for(game_state.current_player)
    
    if len(legal_moves) == 0:
        # No moves available, game is in stalemate or checkmate
        if game_state.is_in_check(game_state.current_player):
            # Checkmate - worst scenario for current player
            return -sys.maxsize if game_state.current_player == maximizing_player else sys.maxsize, None
        else:
            # Stalemate - neutral value 0
            return 0, None
    
    # Initialize best move
    best_move = None
    
    # If it's the maximizing player's turn
    if game_state.current_player == maximizing_player:
        best_score = -sys.maxsize
        
        # Try each move
        for move in legal_moves:
            # Create a copy of the game state to simulate the move
            new_game_state = game_state.copy()
            new_game_state.make_move(move)
            
            # Recursively get score for this move
            score, _ = minimax(new_game_state, depth - 1, maximizing_player)
            
            # Update best score if better
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_score, best_move
    
    # If it's the minimizing player's turn
    else:
        best_score = sys.maxsize
        
        # Try each move
        for move in legal_moves:
            # Create a copy of the game state to simulate the move
            new_game_state = game_state.copy()
            new_game_state.make_move(move)
            
            # Recursively get score for this move
            score, _ = minimax(new_game_state, depth - 1, maximizing_player)
            
            # Update best score if better
            if score < best_score:
                best_score = score
                best_move = move
        
        return best_score, best_move


def minimax_alpha_beta(game_state: GameState, depth, alpha, beta, maximizing_player: Player):
    """
    Minimax algorithm with alpha-beta pruning for efficiency.
    
    Args:
        game_state: The current game state
        depth: How many moves ahead to look
        alpha: The best already explored option for maximizer
        beta: The best already explored option for minimizer
        maximizing_player: The player that is maximizing the score
    
    Returns:
        The best score achievable and the best move to make
    """
    # Base case: reached depth limit or game over
    if depth == 0 or game_state.is_game_over():
        # Return the evaluation score from the perspective of maximizing player
        score = BoardEvaluator.evaluate(game_state.board, maximizing_player)
        return score, None
    
    # Get legal moves for current player
    legal_moves = game_state.all_legal_moves_for(game_state.current_player)
    
    if len(legal_moves) == 0:
        # No moves available, game is in stalemate or checkmate
        if game_state.is_in_check(game_state.current_player):
            # Checkmate - worst scenario for current player
            return -sys.maxsize if game_state.current_player == maximizing_player else sys.maxsize, None
        else:
            # Stalemate - neutral value 0
            return 0, None
    
    # Sort moves for better alpha-beta pruning 
    # (examining likely good moves first improves pruning)
    # This would require move ordering heuristics
    
    # Initialize best move
    best_move = None
    
    # If it's the maximizing player's turn
    if game_state.current_player == maximizing_player:
        best_score = -sys.maxsize
        
        # Try each move
        for move in legal_moves:
            # Create a copy of the game state to simulate the move
            new_game_state = game_state.copy()
            new_game_state.make_move(move)
            
            # Recursively get score for this move
            score, _ = minimax_alpha_beta(new_game_state, depth - 1, alpha, beta, maximizing_player)
            
            # Update best score if better
            if score > best_score:
                best_score = score
                best_move = move
            
            # Update alpha
            alpha = max(alpha, best_score)
            
            # Prune if possible
            if beta <= alpha:
                break
        
        return best_score, best_move
    
    # If it's the minimizing player's turn
    else:
        best_score = sys.maxsize
        
        # Try each move
        for move in legal_moves:
            # Create a copy of the game state to simulate the move
            new_game_state = game_state.copy()
            new_game_state.make_move(move)
            
            # Recursively get score for this move
            score, _ = minimax_alpha_beta(new_game_state, depth - 1, alpha, beta, maximizing_player)
            
            # Update best score if better
            if score < best_score:
                best_score = score
                best_move = move
            
            # Update beta
            beta = min(beta, best_score)
            
            # Prune if possible
            if beta <= alpha:
                break
        
        return best_score, best_move
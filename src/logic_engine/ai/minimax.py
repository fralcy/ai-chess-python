"""
Minimax algorithm implementation using logic programming.
This module provides a logic-based approach to the minimax algorithm
with alpha-beta pruning for chess AI.
"""

import sys
from src.logic.player import Player
from src.logic_engine.predicates import ChessPredicates
from src.logic_engine.logic_board import LogicBoard
from src.logic_engine.logic_game_state import LogicGameState
from src.logic_engine.ai.evaluator import LogicBoardEvaluator

def minimax_logic(game_state, depth, alpha=-sys.maxsize, beta=sys.maxsize, maximizing_player=None, logic_engine=None):
    """
    Minimax algorithm with alpha-beta pruning using logic programming.
    
    Args:
        game_state: The current game state (LogicGameState)
        depth: How many moves ahead to look
        alpha: The best already explored option for maximizer
        beta: The best already explored option for minimizer
        maximizing_player: The player to maximize the score for
        logic_engine: Optional logic engine to use
        
    Returns:
        The best score and the best move
    """
    # If no maximizing player provided, use the current player
    if maximizing_player is None:
        maximizing_player = game_state.current_player
    
    # Base case: reached depth limit or game over
    if depth == 0 or game_state.is_game_over():
        score = LogicBoardEvaluator.evaluate(
            game_state.logic_board,
            maximizing_player,
            logic_engine
        )
        return score, None
    
    # Get legal moves for current player
    legal_moves = game_state.all_legal_moves_for(game_state.current_player)
    
    # If no moves available, evaluate the position
    if not legal_moves:
        # If in check, it's checkmate (worst scenario for current player)
        if game_state.is_in_check(game_state.current_player):
            return -sys.maxsize if game_state.current_player == maximizing_player else sys.maxsize, None
        else:
            # Stalemate - neutral value 0
            return 0, None
    
    # Initialize best move
    best_move = None
    
    # If it's the maximizing player's turn
    if game_state.current_player == maximizing_player:
        best_score = -sys.maxsize
        
        # Order moves for better pruning
        ordered_moves = order_moves(game_state, legal_moves)
        
        # Try each move
        for move in ordered_moves:
            # Create a copy of the game state to simulate the move
            new_game_state = simulate_move(game_state, move)
            
            # Recursively get score for this move
            score, _ = minimax_logic(
                new_game_state,
                depth - 1,
                alpha,
                beta,
                maximizing_player,
                logic_engine
            )
            
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
        
        # Order moves for better pruning
        ordered_moves = order_moves(game_state, legal_moves)
        
        # Try each move
        for move in ordered_moves:
            # Create a copy of the game state to simulate the move
            new_game_state = simulate_move(game_state, move)
            
            # Recursively get score for this move
            score, _ = minimax_logic(
                new_game_state,
                depth - 1,
                alpha,
                beta,
                maximizing_player,
                logic_engine
            )
            
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


def order_moves(game_state, moves):
    """
    Order moves to improve alpha-beta pruning efficiency.
    Capturing moves and checks are examined first.
    
    Args:
        game_state: The current game state
        moves: List of moves to order
        
    Returns:
        Ordered list of moves
    """
    # Assign a score to each move for ordering
    move_scores = []
    
    for move in moves:
        score = 0
        from_pos = move.from_pos
        to_pos = move.to_pos
        
        # Get the piece at the starting position
        piece = game_state.logic_board.get_piece_at(from_pos)
        if not piece:
            continue
            
        piece_type, player = piece
        
        # Check if this is a capturing move
        capture = game_state.logic_board.get_piece_at(to_pos)
        if capture:
            # Capturing more valuable pieces is better
            # MVV-LVA (Most Valuable Victim - Least Valuable Aggressor)
            victim_type, _ = capture
            score += LogicBoardEvaluator.get_piece_value(victim_type) - LogicBoardEvaluator.get_piece_value(piece_type) // 10
        
        # Check if this move gives check
        new_game_state = simulate_move(game_state, move)
        if new_game_state.is_in_check(player.opponent()):
            score += 50  # Prioritize checking moves
        
        # Central squares are generally better
        center_distance = abs(3.5 - to_pos.row) + abs(3.5 - to_pos.column)
        score -= center_distance * 2
        
        # Add to the list with score
        move_scores.append((move, score))
    
    # Sort by score, descending
    move_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return just the moves in order
    return [move for move, _ in move_scores]


def simulate_move(game_state, move):
    """
    Create a copy of the game state and apply the move.
    
    Args:
        game_state: The original game state
        move: The move to apply
        
    Returns:
        A new game state with the move applied
    """
    # Create a copy of the traditional board
    board = game_state.to_traditional_board()
    
    # Create a copy of the logic game state
    new_game_state = LogicGameState(board, game_state.current_player)
    
    # Apply the move to the new state
    new_game_state.make_move(move)
    
    # Return the new state
    return new_game_state
"""
Board evaluation module for the minimax algorithm.
Uses logic programming to evaluate the board position.
"""

from src.logic.player import Player
from src.logic.piece_type import PieceType
from src.logic.position import Position
from src.logic_engine.predicates import ChessPredicates

class LogicBoardEvaluator:
    """
    Logic-based evaluator for chess board positions.
    Uses the logic engine to evaluate the board.
    """
    
    # Piece values (standard chess piece values)
    PIECE_VALUES = {
        PieceType.PAWN: 100,
        PieceType.KNIGHT: 320,
        PieceType.BISHOP: 330,
        PieceType.ROOK: 500,
        PieceType.QUEEN: 900,
        PieceType.KING: 20000  # King is extremely valuable
    }
    
    # Piece-Square tables for positional evaluation
    # These tables encourage pieces to move to good squares
    # Values are from white's perspective - will be flipped for black
    
    # Pawns are encouraged to advance and control the center
    PAWN_TABLE = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]
    ]
    
    # Knights are encouraged to stay near the center and avoid the edges
    KNIGHT_TABLE = [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ]
    
    # Bishops are encouraged to control diagonals and stay away from corners
    BISHOP_TABLE = [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5,  5,  5,  5,  5,-10],
        [-10,  0,  5,  0,  0,  5,  0,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ]
    
    # Rooks are encouraged to control open files and 7th rank
    ROOK_TABLE = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]
    ]
    
    # Queens combine the power of rooks and bishops
    QUEEN_TABLE = [
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [-5,  0,  5,  5,  5,  5,  0, -5],
        [0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]
    ]
    
    # Kings are encouraged to stay protected in the corners in the midgame
    KING_TABLE_MIDGAME = [
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [20, 30, 10,  0,  0, 10, 30, 20]
    ]
    
    # Kings are encouraged to move to the center in the endgame
    KING_TABLE_ENDGAME = [
        [-50,-40,-30,-20,-20,-30,-40,-50],
        [-30,-20,-10,  0,  0,-10,-20,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-30,  0,  0,  0,  0,-30,-30],
        [-50,-30,-30,-30,-30,-30,-30,-50]
    ]
    
    @staticmethod
    def get_piece_value(piece_type):
        """Get the material value of a piece."""
        return LogicBoardEvaluator.PIECE_VALUES.get(piece_type, 0)
    
    @staticmethod
    def get_piece_square_table(piece_type, row, col, player, is_endgame=False):
        """
        Get the position value from the appropriate piece-square table.
        
        Args:
            piece_type: The type of the piece
            row: The row of the piece
            col: The column of the piece
            player: The player that owns the piece
            is_endgame: Whether we're in an endgame position
            
        Returns:
            The position value
        """
        # Reverse row index for black pieces
        if player == Player.BLACK:
            row = 7 - row
        
        if piece_type == PieceType.PAWN:
            return LogicBoardEvaluator.PAWN_TABLE[row][col]
        elif piece_type == PieceType.KNIGHT:
            return LogicBoardEvaluator.KNIGHT_TABLE[row][col]
        elif piece_type == PieceType.BISHOP:
            return LogicBoardEvaluator.BISHOP_TABLE[row][col]
        elif piece_type == PieceType.ROOK:
            return LogicBoardEvaluator.ROOK_TABLE[row][col]
        elif piece_type == PieceType.QUEEN:
            return LogicBoardEvaluator.QUEEN_TABLE[row][col]
        elif piece_type == PieceType.KING:
            if is_endgame:
                return LogicBoardEvaluator.KING_TABLE_ENDGAME[row][col]
            else:
                return LogicBoardEvaluator.KING_TABLE_MIDGAME[row][col]
        return 0
    
    @staticmethod
    def evaluate(logic_board, player, logic_engine=None):
        """
        Evaluate the board from perspective of the given player.
        
        Args:
            logic_board: The logic board to evaluate
            player: The player to evaluate for
            logic_engine: Optional logic engine to use
            
        Returns:
            A score for the position
        """
        # Use the board's logic engine if none provided
        engine = logic_engine or logic_board.engine
        
        # Get the opponent
        opponent = player.opponent()
        
        # Check for checkmate and stalemate
        is_checkmate = False
        is_stalemate = False
        
        checkmate_results = engine.query(
            ChessPredicates.CHECKMATE,
            player
        )
        if checkmate_results:
            return -100000  # Worst possible score
        
        checkmate_results = engine.query(
            ChessPredicates.CHECKMATE,
            opponent
        )
        if checkmate_results:
            return 100000  # Best possible score
        
        stalemate_results = engine.query(
            ChessPredicates.STALEMATE,
            player
        )
        if stalemate_results or engine.query(ChessPredicates.STALEMATE, opponent):
            return 0  # Draw
        
        # Calculate material score
        material_score = LogicBoardEvaluator.calculate_material_score(engine, player, opponent)
        
        # Calculate positional score
        positional_score = LogicBoardEvaluator.calculate_positional_score(engine, player, opponent)
        
        # Check if we're in the endgame
        total_material = material_score[0] + material_score[1]
        is_endgame = total_material < 3000  # Arbitrary threshold
        
        # Calculate mobility (number of legal moves)
        mobility_score = LogicBoardEvaluator.calculate_mobility_score(engine, player, opponent)
        
        # Calculate pawn structure score
        pawn_structure_score = LogicBoardEvaluator.calculate_pawn_structure_score(engine, player, opponent)
        
        # Calculate king safety score
        king_safety_score = LogicBoardEvaluator.calculate_king_safety_score(engine, player, opponent, is_endgame)
        
        # Calculate center control score
        center_control_score = LogicBoardEvaluator.calculate_center_control_score(engine, player, opponent)
        
        # Combine all factors with appropriate weights
        # The weights can be adjusted based on playing style and testing
        final_score = (
            material_score[0] - material_score[1] +
            (positional_score[0] - positional_score[1]) * 0.1 +
            (mobility_score[0] - mobility_score[1]) * 0.2 +
            (pawn_structure_score[0] - pawn_structure_score[1]) * 0.3 +
            (king_safety_score[0] - king_safety_score[1]) * (0.5 if not is_endgame else 0.1) +
            (center_control_score[0] - center_control_score[1]) * 0.4
        )
        
        return final_score
    
    @staticmethod
    def calculate_material_score(engine, player, opponent):
        """
        Calculate the material score for both players.
        
        Args:
            engine: The logic engine
            player: The player to evaluate for
            opponent: The opponent player
            
        Returns:
            A tuple (player_score, opponent_score)
        """
        var_piece_type = engine.variable("PieceType")
        var_row = engine.variable("Row")
        var_col = engine.variable("Col")
        
        # Count pieces for player
        player_material = 0
        player_pieces = engine.query(
            ChessPredicates.PIECE_AT,
            var_piece_type, player, var_row, var_col
        )
        for binding in player_pieces:
            piece_type = binding.get("PieceType")
            player_material += LogicBoardEvaluator.get_piece_value(piece_type)
        
        # Count pieces for opponent
        opponent_material = 0
        opponent_pieces = engine.query(
            ChessPredicates.PIECE_AT,
            var_piece_type, opponent, var_row, var_col
        )
        for binding in opponent_pieces:
            piece_type = binding.get("PieceType")
            opponent_material += LogicBoardEvaluator.get_piece_value(piece_type)
        
        return (player_material, opponent_material)
    
    @staticmethod
    def calculate_positional_score(engine, player, opponent):
        """
        Calculate the positional score for both players.
        
        Args:
            engine: The logic engine
            player: The player to evaluate for
            opponent: The opponent player
            
        Returns:
            A tuple (player_score, opponent_score)
        """
        var_piece_type = engine.variable("PieceType")
        var_row = engine.variable("Row")
        var_col = engine.variable("Col")
        
        # Calculate positional score for player
        player_positional = 0
        player_pieces = engine.query(
            ChessPredicates.PIECE_AT,
            var_piece_type, player, var_row, var_col
        )
        for binding in player_pieces:
            piece_type = binding.get("PieceType")
            row = binding.get("Row")
            col = binding.get("Col")
            player_positional += LogicBoardEvaluator.get_piece_square_table(
                piece_type, row, col, player
            )
        
        # Calculate positional score for opponent
        opponent_positional = 0
        opponent_pieces = engine.query(
            ChessPredicates.PIECE_AT,
            var_piece_type, opponent, var_row, var_col
        )
        for binding in opponent_pieces:
            piece_type = binding.get("PieceType")
            row = binding.get("Row")
            col = binding.get("Col")
            opponent_positional += LogicBoardEvaluator.get_piece_square_table(
                piece_type, row, col, opponent
            )
        
        return (player_positional, opponent_positional)
    
    @staticmethod
    def calculate_mobility_score(engine, player, opponent):
        """
        Calculate the mobility score (number of legal moves) for both players.
        
        Args:
            engine: The logic engine
            player: The player to evaluate for
            opponent: The opponent player
            
        Returns:
            A tuple (player_score, opponent_score)
        """
        var_piece_type = engine.variable("PieceType")
        var_from_row = engine.variable("FromRow")
        var_from_col = engine.variable("FromCol")
        var_to_row = engine.variable("ToRow")
        var_to_col = engine.variable("ToCol")
        
        # Count legal moves for player
        player_mobility = 0
        player_pieces = engine.query(
            ChessPredicates.PIECE_AT,
            var_piece_type, player, var_from_row, var_from_col
        )
        for binding in player_pieces:
            piece_type = binding.get("PieceType")
            from_row = binding.get("FromRow")
            from_col = binding.get("FromCol")
            
            # Count legal moves for this piece
            legal_moves = engine.query(
                ChessPredicates.CAN_MOVE,
                piece_type, player, from_row, from_col, var_to_row, var_to_col
            )
            player_mobility += len(legal_moves)
        
        # Count legal moves for opponent
        opponent_mobility = 0
        opponent_pieces = engine.query(
            ChessPredicates.PIECE_AT,
            var_piece_type, opponent, var_from_row, var_from_col
        )
        for binding in opponent_pieces:
            piece_type = binding.get("PieceType")
            from_row = binding.get("FromRow")
            from_col = binding.get("FromCol")
            
            # Count legal moves for this piece
            legal_moves = engine.query(
                ChessPredicates.CAN_MOVE,
                piece_type, opponent, from_row, from_col, var_to_row, var_to_col
            )
            opponent_mobility += len(legal_moves)
        
        return (player_mobility * 10, opponent_mobility * 10)
    
    @staticmethod
    def calculate_pawn_structure_score(engine, player, opponent):
        """
        Calculate the pawn structure score for both players.
        
        Args:
            engine: The logic engine
            player: The player to evaluate for
            opponent: The opponent player
            
        Returns:
            A tuple (player_score, opponent_score)
        """
        var_row = engine.variable("Row")
        var_col = engine.variable("Col")
        
        # Find all pawns
        player_pawns = engine.query(
            ChessPredicates.PIECE_AT,
            PieceType.PAWN, player, var_row, var_col
        )
        
        opponent_pawns = engine.query(
            ChessPredicates.PIECE_AT,
            PieceType.PAWN, opponent, var_row, var_col
        )
        
        # Calculate pawn structure score
        player_score = LogicBoardEvaluator._evaluate_pawn_structure(player_pawns, player)
        opponent_score = LogicBoardEvaluator._evaluate_pawn_structure(opponent_pawns, opponent)
        
        return (player_score, opponent_score)
    
    @staticmethod
    def _evaluate_pawn_structure(pawns, player):
        """
        Evaluate the pawn structure for a player.
        
        Args:
            pawns: List of pawn positions
            player: The player that owns the pawns
            
        Returns:
            A score for the pawn structure
        """
        score = 0
        
        # Check for doubled pawns (same column)
        columns = [binding.get("Col") for binding in pawns]
        column_counts = {}
        for col in columns:
            column_counts[col] = column_counts.get(col, 0) + 1
        
        # Penalty for doubled pawns
        for col, count in column_counts.items():
            if count > 1:
                score -= (count - 1) * 20
        
        # Bonus for pawn chains
        pawn_positions = [(binding.get("Row"), binding.get("Col")) for binding in pawns]
        for row, col in pawn_positions:
            # Check if there's a supporting pawn
            if player == Player.WHITE:
                if (row + 1, col - 1) in pawn_positions or (row + 1, col + 1) in pawn_positions:
                    score += 10
            else:
                if (row - 1, col - 1) in pawn_positions or (row - 1, col + 1) in pawn_positions:
                    score += 10
        
        # Bonus for passed pawns
        for binding in pawns:
            row = binding.get("Row")
            col = binding.get("Col")
            
            # Check if it's a passed pawn
            is_passed = True
            if player == Player.WHITE:
                # For white, check if there are any black pawns in front
                for opponent_row in range(row - 1, -1, -1):
                    for opponent_col in range(max(0, col - 1), min(8, col + 2)):
                        if (opponent_row, opponent_col) in pawn_positions:
                            is_passed = False
                            break
            else:
                # For black, check if there are any white pawns in front
                for opponent_row in range(row + 1, 8):
                    for opponent_col in range(max(0, col - 1), min(8, col + 2)):
                        if (opponent_row, opponent_col) in pawn_positions:
                            is_passed = False
                            break
            
            if is_passed:
                # Bonus based on how far advanced the pawn is
                if player == Player.WHITE:
                    score += (7 - row) * 20
                else:
                    score += row * 20
        
        return score
    
    @staticmethod
    def calculate_king_safety_score(engine, player, opponent, is_endgame):
        """
        Calculate the king safety score for both players.
        
        Args:
            engine: The logic engine
            player: The player to evaluate for
            opponent: The opponent player
            is_endgame: Whether we're in an endgame position
            
        Returns:
            A tuple (player_score, opponent_score)
        """
        var_row = engine.variable("Row")
        var_col = engine.variable("Col")
        
        # Find king positions
        player_king = engine.query(
            ChessPredicates.PIECE_AT,
            PieceType.KING, player, var_row, var_col
        )
        
        opponent_king = engine.query(
            ChessPredicates.PIECE_AT,
            PieceType.KING, opponent, var_row, var_col
        )
        
        if not player_king or not opponent_king:
            return (0, 0)
        
        player_king_row = player_king[0].get("Row")
        player_king_col = player_king[0].get("Col")
        opponent_king_row = opponent_king[0].get("Row")
        opponent_king_col = opponent_king[0].get("Col")
        
        # Different evaluations based on game phase
        if is_endgame:
            # In endgame, king should be active and move to the center
            player_score = LogicBoardEvaluator._evaluate_king_endgame(
                player_king_row, player_king_col, opponent_king_row, opponent_king_col)
            opponent_score = LogicBoardEvaluator._evaluate_king_endgame(
                opponent_king_row, opponent_king_col, player_king_row, player_king_col)
        else:
            # In midgame, king should be safe
            player_score = LogicBoardEvaluator._evaluate_king_safety(
                engine, player, player_king_row, player_king_col)
            opponent_score = LogicBoardEvaluator._evaluate_king_safety(
                engine, opponent, opponent_king_row, opponent_king_col)
        
        return (player_score, opponent_score)
    
    @staticmethod
    def _evaluate_king_safety(engine, player, king_row, king_col):
        """
        Evaluate king safety in the midgame.
        
        Args:
            engine: The logic engine
            player: The player whose king to evaluate
            king_row: The row of the king
            king_col: The column of the king
            
        Returns:
            A score for king safety
        """
        score = 0
        
        # Check if king is in check
        if engine.query(ChessPredicates.IN_CHECK, player):
            score -= 50
        
        # Check attacked squares around the king
        opponent = player.opponent()
        attacked_count = 0
        
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                # Skip the king's own square
                if row_offset == 0 and col_offset == 0:
                    continue
                
                # Get the adjacent square
                adj_row = king_row + row_offset
                adj_col = king_col + col_offset
                
                # Check if the square is on the board
                if 0 <= adj_row < 8 and 0 <= adj_col < 8:
                    # Check if the square is attacked
                    if engine.query(ChessPredicates.SQUARE_ATTACKED, opponent, adj_row, adj_col):
                        attacked_count += 1
        
        # Penalty for attacked squares around the king
        score -= attacked_count * 10
        
        # Bonus for pawn shield in front of the king
        var_row = engine.variable("Row")
        var_col = engine.variable("Col")
        
        # Define the area in front of the king based on color
        shield_squares = []
        if player == Player.WHITE:
            # For white, the shield is above the king
            base_row = king_row - 1
            for r in range(base_row, max(-1, base_row - 2), -1):
                for c in range(max(0, king_col - 1), min(8, king_col + 2)):
                    shield_squares.append((r, c))
        else:
            # For black, the shield is below the king
            base_row = king_row + 1
            for r in range(base_row, min(8, base_row + 2)):
                for c in range(max(0, king_col - 1), min(8, king_col + 2)):
                    shield_squares.append((r, c))
        
        # Count pawns in the shield area
        pawn_count = 0
        for row, col in shield_squares:
            pawn_results = engine.query(
                ChessPredicates.PIECE_AT,
                PieceType.PAWN, player, row, col
            )
            if pawn_results:
                pawn_count += 1
        
        # Bonus for pawn shield
        score += pawn_count * 15
        
        # Penalty for open files near the king
        for col_offset in range(-1, 2):
            col = king_col + col_offset
            
            if 0 <= col < 8:
                file_empty = True
                for row in range(8):
                    square_results = engine.query(
                        ChessPredicates.PIECE_AT,
                        PieceType.PAWN, player, row, col
                    )
                    if square_results:
                        file_empty = False
                        break
                
                if file_empty:
                    score -= 20
        
        return score
    
    @staticmethod
    def _evaluate_king_endgame(king_row, king_col, opponent_king_row, opponent_king_col):
        """
        Evaluate king position in the endgame.
        
        Args:
            king_row: The row of the king
            king_col: The column of the king
            opponent_king_row: The row of the opponent's king
            opponent_king_col: The column of the opponent's king
            
        Returns:
            A score for king position in endgame
        """
        score = 0
        
        # Distance to center (0-7 scale, lower is better)
        center_distance = max(abs(3.5 - king_row), abs(3.5 - king_col))
        score += (4 - center_distance) * 10
        
        # Distance to opponent king (higher is worse in an endgame)
        king_distance = max(abs(king_row - opponent_king_row), abs(king_col - opponent_king_col))
        
        # We want our king to be close to the opponent's king to restrict its movement
        # But we also don't want to be too close to avoid stalemate
        if king_distance <= 2:
            score += 20
        else:
            score -= (king_distance - 2) * 5
        
        return score
    
    @staticmethod
    def calculate_center_control_score(engine, player, opponent):
        """
        Calculate the center control score for both players.
        
        Args:
            engine: The logic engine
            player: The player to evaluate for
            opponent: The opponent player
            
        Returns:
            A tuple (player_score, opponent_score)
        """
        # Define the center squares
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        extended_center = [(2, 2), (2, 3), (2, 4), (2, 5),
                         (3, 2), (3, 5), (4, 2), (4, 5),
                         (5, 2), (5, 3), (5, 4), (5, 5)]
        
        var_piece_type = engine.variable("PieceType")
        
        # Count pieces in the center
        player_center = 0
        opponent_center = 0
        
        for row, col in center_squares:
            # Check if player controls this square
            player_results = engine.query(
                ChessPredicates.PIECE_AT,
                var_piece_type, player, row, col
            )
            if player_results:
                player_center += 20
            
            # Check if opponent controls this square
            opponent_results = engine.query(
                ChessPredicates.PIECE_AT,
                var_piece_type, opponent, row, col
            )
            if opponent_results:
                opponent_center += 20
            
            # Check attacks on this square
            if engine.query(ChessPredicates.SQUARE_ATTACKED, player, row, col):
                player_center += 10
            if engine.query(ChessPredicates.SQUARE_ATTACKED, opponent, row, col):
                opponent_center += 10
        
        # Count pieces in the extended center
        for row, col in extended_center:
            # Check if player controls this square
            player_results = engine.query(
                ChessPredicates.PIECE_AT,
                var_piece_type, player, row, col
            )
            if player_results:
                player_center += 10
            
            # Check if opponent controls this square
            opponent_results = engine.query(
                ChessPredicates.PIECE_AT,
                var_piece_type, opponent, row, col
            )
            if opponent_results:
                opponent_center += 10
            
            # Check attacks on this square
            if engine.query(ChessPredicates.SQUARE_ATTACKED, player, row, col):
                player_center += 5
            if engine.query(ChessPredicates.SQUARE_ATTACKED, opponent, row, col):
                opponent_center += 5
        
        return (player_center, opponent_center)
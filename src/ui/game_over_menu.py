import pygame
import sys
import os
from src.logic.game_state import GameState
# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class GameOverMenu:
    """A simple game over menu for the chess game."""
    
    # Colors
    BACKGROUND_COLOR = (0, 0, 0, 200)  # More opaque black
    TEXT_COLOR = (255, 215, 0)  # Gold for text
    BUTTON_COLOR = (70, 130, 180)  # Steel blue
    BUTTON_HOVER_COLOR = (100, 149, 237)  # Cornflower blue
    BUTTON_TEXT_COLOR = (255, 255, 255)  # White
    
    def __init__(self, screen, game_state: GameState):
        """Initialize the game over menu.
        
        Args:
            screen: The pygame screen to draw on
            winner: The player who won (Player enum)
            reason: The reason the game ended (EndReason enum)
        """
        self.screen = screen
        self.winner = game_state.result.winner
        self.reason = game_state.result.end_reason
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Create fancy fonts - try to use nicer fonts if available
        try:
            self.winner_font = pygame.font.Font("freesansbold.ttf", 46)
        except:
            self.winner_font = pygame.font.SysFont('Arial', 46, bold=True)
            
        try:
            self.text_font = pygame.font.Font("freesansbold.ttf", 32)
        except:
            self.text_font = pygame.font.SysFont('Arial', 32)
            
        try:
            self.button_font = pygame.font.Font("freesansbold.ttf", 24)
        except:
            self.button_font = pygame.font.SysFont('Arial', 24)
        
        # Create rounded, modern buttons
        button_width = 160
        button_height = 60
        button_y = self.screen_height // 2 + 70
        
        self.replay_button = pygame.Rect(
            self.screen_width // 2 - button_width - 30,
            button_y,
            button_width,
            button_height
        )
        
        self.exit_button = pygame.Rect(
            self.screen_width // 2 + 30,
            button_y,
            button_width,
            button_height
        )
    
    def draw(self):
        """Draw the game over menu."""
        # Create a semi-transparent overlay with gradient effect
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill(self.BACKGROUND_COLOR)
        self.screen.blit(overlay, (0, 0))
        
        # Draw a decorative panel in the center
        panel_width = self.screen_width * 0.7
        panel_height = self.screen_height * 0.5
        panel_rect = pygame.Rect(
            (self.screen_width - panel_width) // 2,
            (self.screen_height - panel_height) // 2,
            panel_width,
            panel_height
        )
        pygame.draw.rect(self.screen, (30, 30, 30, 220), panel_rect, border_radius=15)
        
        # Add a border to the panel
        pygame.draw.rect(self.screen, (100, 100, 100, 150), panel_rect, width=2, border_radius=15)
        
        # Draw winner text (larger and centered)
        if self.winner is not None:
            from logic.player import Player
            winner_text = ""
            if self.winner == Player.WHITE:
                winner_text = "White wins!"
            elif self.winner == Player.BLACK:
                winner_text = "Black wins!"
            else:
                winner_text = "Draw!"
            
            winner_surface = self.winner_font.render(winner_text, True, self.TEXT_COLOR)
            winner_rect = winner_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 60))
            self.screen.blit(winner_surface, winner_rect)
        
        # Draw reason text
        if self.reason is not None:
            from logic.end_reason import EndReason
            reason_text = ""
            if self.reason == EndReason.CHECKMATE:
                reason_text = "Checkmate"
            elif self.reason == EndReason.STALEMATE:
                reason_text = "Stalemate"
            elif self.reason == EndReason.FIFTY_MOVE_RULE:
                reason_text = "Fifty move rule"
            elif self.reason == EndReason.INSUFFICIENT_MATERIAL:
                reason_text = "Insufficient material"
            elif self.reason == EndReason.THREEFOLD_REPETITION:
                reason_text = "Threefold repetition"
            
            reason_surface = self.text_font.render(reason_text, True, (180, 180, 180))
            reason_rect = reason_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(reason_surface, reason_rect)
        
        # Draw buttons with improved appearance
        mouse_pos = pygame.mouse.get_pos()
        
        # Replay button (with hover effect and shadow)
        replay_color = self.BUTTON_HOVER_COLOR if self.replay_button.collidepoint(mouse_pos) else self.BUTTON_COLOR
        
        # Button shadow
        shadow_rect = self.replay_button.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (20, 20, 20), shadow_rect, border_radius=10)
        
        # Main button
        pygame.draw.rect(self.screen, replay_color, self.replay_button, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255, 100), self.replay_button, width=2, border_radius=10)
        replay_text = self.button_font.render("Play Again", True, self.BUTTON_TEXT_COLOR)
        replay_text_rect = replay_text.get_rect(center=self.replay_button.center)
        self.screen.blit(replay_text, replay_text_rect)
        
        # Exit button (with hover effect and shadow)
        exit_color = self.BUTTON_HOVER_COLOR if self.exit_button.collidepoint(mouse_pos) else self.BUTTON_COLOR
        
        # Button shadow
        shadow_rect = self.exit_button.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (20, 20, 20), shadow_rect, border_radius=10)
        
        # Main button
        pygame.draw.rect(self.screen, exit_color, self.exit_button, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255, 100), self.exit_button, width=2, border_radius=10)
        exit_text = self.button_font.render("Exit", True, self.BUTTON_TEXT_COLOR)
        exit_text_rect = exit_text.get_rect(center=self.exit_button.center)
        self.screen.blit(exit_text, exit_text_rect)

    def handle_restart_click(self, event):
        """Handle clicks on the replay button."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.replay_button.collidepoint(event.pos):
                return True
        return False
    
    def handle_exit_click(self, event):
        """Handle clicks on the exit button."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.exit_button.collidepoint(event.pos):
                return True
        return False
    
    def get_winner_text(self):
        from src.logic.player import Player
        if self.winner == Player.WHITE:
            return "White wins!"
        elif self.winner == Player.BLACK:
            return "Black wins!"
        else:
            return "It's a draw!"
        
    def player_string(self, player):
        from src.logic.player import Player
        if player == Player.WHITE:
            return "White"
        elif player == Player.BLACK:
            return "Black"
        else:
            return "Unknown"
        
    def get_reason_text(self, end_reason, current_player):
        from src.logic.end_reason import EndReason
        from src.logic.player import Player
        match end_reason:
            case EndReason.Stalemate:
                return f"STALEMATE = {self.player_string(current_player)} CAN'T MOVE"
            case EndReason.Checkmate:
                return f"CHECKMATE = {self.player_string(current_player)} CAN'T MOVE"
            case EndReason.FiftyMoveRule:
                return "FIFTY-MOVE RULE"
            case EndReason.InsufficientMaterial:
                return "INSUFFICIENT MATERIAL"
            case EndReason.ThreefoldRepetition:
                return "THREEFOLD REPETITION"
            case _:
                return ""
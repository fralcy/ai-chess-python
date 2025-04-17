"""
Asset loading and management
"""

import pygame
import os
from src.constants import PIECE_IMAGES, SQUARE_SIZE

# Dictionary to cache loaded images
_piece_surfaces = {}

def load_piece_image(piece_type, color):
    """Load a piece image from file or cache"""
    key = (piece_type, color)
    
    # If already loaded, return from cache
    if key in _piece_surfaces:
        return _piece_surfaces[key]
    
    # Check if the image file exists
    image_path = PIECE_IMAGES.get(key, None)
    if not image_path or not os.path.exists(image_path):
        # Create a fallback text-based surface
        surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        font = pygame.font.SysFont('Arial', 36)
        text_color = (0, 0, 0) if color == 'white' else (255, 255, 255)
        text = font.render(piece_type, True, text_color)
        text_rect = text.get_rect(center=(SQUARE_SIZE // 2, SQUARE_SIZE // 2))
        surface.blit(text, text_rect)
        _piece_surfaces[key] = surface
        return surface
    
    # Load the image from file
    try:
        # Load and scale the image to fit the square
        original = pygame.image.load(image_path).convert_alpha()
        scaled = pygame.transform.scale(original, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
        
        # Create a surface with proper padding
        surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        # Center the piece image on the square
        surface.blit(scaled, (5, 5))
        
        # Cache and return
        _piece_surfaces[key] = surface
        return surface
    
    except pygame.error:
        # Create a fallback text-based surface
        surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        font = pygame.font.SysFont('Arial', 36)
        text_color = (0, 0, 0) if color == 'white' else (255, 255, 255)
        text = font.render(piece_type, True, text_color)
        text_rect = text.get_rect(center=(SQUARE_SIZE // 2, SQUARE_SIZE // 2))
        surface.blit(text, text_rect)
        _piece_surfaces[key] = surface
        return surface

def clear_cache():
    """Clear the image cache"""
    _piece_surfaces.clear()
"""
Utility functions for the chess game.
"""

import os
import sys
import shutil

def create_default_assets():
    """
    Create default assets if they don't exist.
    This function generates some very basic placeholder images for chess pieces.
    """
    from pygame import Surface, draw, image, Color
    
    # Ensure assets directory exists
    os.makedirs('assets/images', exist_ok=True)
    
    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    # Size of the images
    SIZE = (80, 80)
    
    # Piece types and colors
    pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
    colors = ['white', 'black']
    
    # Check which images are missing
    missing_images = []
    for color in colors:
        for piece in pieces:
            filename = f'assets/images/{color}_{piece}.png'
            if not os.path.exists(filename):
                missing_images.append((color, piece, filename))
    
    # If no images are missing, return
    if not missing_images:
        return
    
    print(f"Creating {len(missing_images)} placeholder images for chess pieces...")
    
    # Create placeholder images for missing pieces
    for color, piece, filename in missing_images:
        # Create a surface
        surface = Surface(SIZE)
        
        # Fill with the background color (opposite of piece color)
        bg_color = BLACK if color == 'white' else WHITE
        surface.fill(bg_color)
        
        # Get piece color
        piece_color = WHITE if color == 'white' else BLACK
        
        # Draw a basic shape based on the piece type
        if piece == 'pawn':
            # Draw a simple circle
            draw.circle(surface, piece_color, (SIZE[0]//2, SIZE[1]//2), SIZE[0]//3)
        elif piece == 'knight':
            # Draw a triangle
            points = [(SIZE[0]//4, SIZE[1]//4*3), (SIZE[0]//2, SIZE[1]//4),
                      (SIZE[0]//4*3, SIZE[1]//4*3)]
            draw.polygon(surface, piece_color, points)
        elif piece == 'bishop':
            # Draw a diamond
            points = [(SIZE[0]//2, SIZE[1]//4), (SIZE[0]//4*3, SIZE[1]//2),
                      (SIZE[0]//2, SIZE[1]//4*3), (SIZE[0]//4, SIZE[1]//2)]
            draw.polygon(surface, piece_color, points)
        elif piece == 'rook':
            # Draw a square
            rect = (SIZE[0]//4, SIZE[1]//4, SIZE[0]//2, SIZE[1]//2)
            draw.rect(surface, piece_color, rect)
        elif piece == 'queen':
            # Draw a circle with a smaller circle inside
            draw.circle(surface, piece_color, (SIZE[0]//2, SIZE[1]//2), SIZE[0]//3)
            draw.circle(surface, bg_color, (SIZE[0]//2, SIZE[1]//2), SIZE[0]//6)
        elif piece == 'king':
            # Draw a cross
            draw.line(surface, piece_color, (SIZE[0]//2, SIZE[1]//4),
                      (SIZE[0]//2, SIZE[1]//4*3), SIZE[0]//8)
            draw.line(surface, piece_color, (SIZE[0]//4, SIZE[1]//2),
                      (SIZE[0]//4*3, SIZE[1]//2), SIZE[0]//8)
        
        # Save the image
        try:
            image.save(surface, filename)
            print(f"Created placeholder image: {filename}")
        except Exception as e:
            print(f"Error creating placeholder image {filename}: {e}")

def ensure_assets_directory():
    """
    Ensure the assets directory exists for the chess piece images.
    Creates default assets if needed.
    """
    # Create assets directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    os.makedirs('assets/images', exist_ok=True)
    
    # Check if there are any PNG images
    image_files = [f for f in os.listdir('assets/images') if f.endswith('.png')]
    
    # If there are no images, create default ones
    if not image_files:
        print("No chess piece images found. Creating placeholder images...")
        try:
            import pygame
            # Initialize pygame to create surfaces
            if not pygame.get_init():
                pygame.init()
            # Create default assets
            create_default_assets()
        except Exception as e:
            print(f"Error creating placeholder images: {e}")
            print("Chess pieces will be displayed as simple shapes.")
            print("For full visual experience, add images like 'white_pawn.png', 'black_king.png', etc.")
    else:
        print(f"Found {len(image_files)} chess piece images in assets/images directory.")
# Creates a chess game and renders the board
# Handles user input and updates the board
# Displays the game result

import pygame
from game import Game

py_game = None
surface = None
game = None
last_move = []
selected_pos = None
style = {
    "piece_style": "basic",
    "light_square": (235, 236, 208),
    "dark_square": (119, 149, 86),
    "selected_square": (212, 108, 81),
    "legal_move": (212, 108, 81),
    "last_move": (246, 246, 105),
}

def render_board():
    
    surface.fill((100, 100, 100))
    
    # Draw the checkerboard
    for i in range(8):
        for j in range(8):
            x = i * 100 + 50
            y = j * 100
            
            # Draw base color
            if (i + j) % 2 == 0:
                pygame.draw.rect(surface, style["light_square"], (x,y,100,100))
            else:
                pygame.draw.rect(surface, style["dark_square"], (x,y,100,100))
                
            # Highlight last move
            if (i,j) in last_move:
                pygame.draw.rect(surface, style["last_move"], (x,y,100,100))
                
            # Highlight if selected, legal, or last move
            if selected_pos is not None:
                if (i,j) == selected_pos:
                    pygame.draw.rect(surface, style["selected_square"], (x,y,100,100))
                elif (i,j) in game.get_piece(selected_pos).get_legal_moves():
                    pygame.draw.rect(surface, style["legal_move"], (x,y,100,100))
                    
    # Write the letters and numbers
    for i in range(8):
        # pygame.draw.rect(surface, (0, 0, 0), (i * 100 + 50, 800, 100, 50))
        # pygame.draw.rect(surface, (0, 0, 0), (0, i * 100, 50, 100))
        font = pygame.font.SysFont("sans-serif", 30)
        text = font.render(chr(97 + i), True, (255, 255, 255))
        surface.blit(text, (i * 100 + 50 + (100 - text.get_width()) / 2, 800 + (50 - text.get_height()) / 2))
        text = font.render(str(8 - i), True, (255, 255, 255))
        surface.blit(text, (25 - text.get_width() / 2, i * 100 + (100 - text.get_height()) / 2))
                
def render_piece(piece, pos):
    (i,j) = pos
    
    icon = None
    
    if style["piece_style"] == "text":
        font = pygame.font.SysFont("sans-serif", 50)
        icon = font.render(piece.icons[piece.color == "white"], True, (0, 0, 0))
    else:
        icon = pygame.image.load('../pieces/' + style["piece_style"] + '/' + piece.name + "_" + piece.color + '.png')
        icon = pygame.transform.scale(icon, (100, 100))
        
    x = i * 100 + 50 + (100 - icon.get_width()) / 2
    y = j * 100 + (100 - icon.get_height()) / 2
    
    if pos == selected_pos:
        (mouse_x,mouse_y) = pygame.mouse.get_pos()
        x = mouse_x - icon.get_width() / 2
        y = mouse_y - icon.get_height() / 2
        
    surface.blit(icon, (x, y))
                
def render_pieces():
    for i in range(8):
        for j in range(8):
            piece = game.pieces[i][j]
            if piece is not None:
                render_piece(piece, (i,j))
                    
                

def render_game():
    
    render_board()
    render_pieces()
    
def handle_click():
    
    global selected_pos, last_move
    
    # Get mouse position
    (mouse_x,mouse_y) = pygame.mouse.get_pos()
    
    # Get the position of the clicked square
    i = (mouse_x - 50) // 100
    j = mouse_y // 100
    
    if (i < 0 or i > 7 or j < 0 or j > 7):
        return
    
    # If a piece is selected, move it or deselect it
    if selected_pos is not None:
        # Get piece
        piece = game.get_piece(selected_pos)
        
        # Get legal moves
        moves = piece.get_legal_moves()
        
        # If the move is legal, move the piece
        if (i,j) in moves:
            game.move_piece(selected_pos, (i,j))
            last_move = [selected_pos, (i,j)]
            
        # Deselect    
        selected_pos = None
            
    # If no piece is selected, select the clicked piece
    else:
        # Get piece
        piece = game.get_piece((i,j))
        
        # If the piece is not empty and is the current player's piece, select it
        if piece is not None and piece.color == game.turn:
            selected_pos = (i,j)
        
    
def __main__():
    global game, surface, last_move, selected_pos, py_game
    
    game = Game()
    py_game = pygame.init()
    last_move = []
    selected_pos = None
    
    run = True
    
    surface = pygame.display.set_mode((850, 850))
    pygame.display.set_caption("Chess")
    
    render_game()   
    
    while run:

        # Handle events
        for event in pygame.event.get():

            # Quit
            if event.type == pygame.QUIT:
                run = False
                
            # Mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_click()
            
            # Mouse move
            if event.type == pygame.MOUSEMOTION and selected_pos is not None:
                pass
                
        # Render the game
        render_game()
        pygame.display.flip() 
        
    pygame.quit()
        
        
if __name__ == "__main__":
    __main__()
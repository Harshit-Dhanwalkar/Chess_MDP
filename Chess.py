<<<<<<< HEAD
# Ganesh was here
# Harshit was here again for 3rd time 
=======
#Ganesh was here
#Harshit was here
#new
>>>>>>> 3e3cddac1aa285f93849be2610b26b0887faa174

import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()
running = True
LIGHT_SQUARE = (245, 203, 167)
DARK_SQUARE = (87, 65, 18)
GRID_COLOR = (0, 0, 0)

# Assuming these are your piece lists
black_pieces = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn',
                'rook', 'rook', 'knight', 'knight', 'bishop', 'bishop', 'queen', 'king']

white_pieces = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn',
                'rook', 'rook', 'knight', 'knight', 'bishop', 'bishop', 'queen', 'king']

# Assuming these are your initial piece positions
black_location = [
    ['pawnB1', 1, 0], ['pawnB2', 1, 1], ['pawnB3', 1, 2], ['pawnB4', 1, 3],
    ['pawnB5', 1, 4], ['pawnB6', 1, 5], ['pawnB7', 1, 6], ['pawnB8', 1, 7],
    ['rookB1', 0, 0], ['rookB2', 0, 7], ['knightB1', 0, 1], ['knightB2', 0, 6],
    ['bishopB1', 0, 2], ['bishopB2', 0, 5], ['queenB1', 0, 3], ['kingB1', 0, 4]
]

<<<<<<< HEAD
white_location = [
    ['pawnW1', 6, 0], ['pawnW2', 6, 1], ['pawnW3', 6, 2], ['pawnW4', 6, 3],
    ['pawnW5', 6, 4], ['pawnW6', 6, 5], ['pawnW7', 6, 6], ['pawnW8', 6, 7],
    ['rookW1', 7, 0], ['rookW2', 7, 7], ['knightW1', 7, 1], ['knightW2', 7, 6],
    ['bishopW1', 7, 2], ['bishopW2', 7, 5], ['queenW1', 7, 3], ['kingW1', 7, 4]
]
=======
# Add a dictionary to store the state of each piece
# Key format: (row, column, piece_type, identifier)
piece_state = {}

captured_piece_black = []
>>>>>>> 3e3cddac1aa285f93849be2610b26b0887faa174

def load_image(img_name):
    IMAGE_DIR = "./Pieces_PNG/"
    img_path = IMAGE_DIR + img_name
    print(f"Loading image: {img_path}")
    try:
        return pygame.image.load(img_path)
    except pygame.error as e:
        print(f"Error loading image {img_name}: {e}")
        raise SystemExit


black_pieces_images = {
    'pawn': pygame.transform.scale(load_image('bP.png'), (80, 80)),
    'rook': pygame.transform.scale(load_image('bR.png'), (80, 80)),
    'knight': pygame.transform.scale(load_image('bN.png'), (80, 80)),
    'bishop': pygame.transform.scale(load_image('bB.png'), (80, 80)),
    'queen': pygame.transform.scale(load_image('bQ.png'), (80, 80)),
    'king': pygame.transform.scale(load_image('bK.png'), (80, 80)),
}

white_pieces_images = {
    'pawn': pygame.transform.scale(load_image('wP.png'), (80, 80)),
    'rook': pygame.transform.scale(load_image('wR.png'), (80, 80)),
    'knight': pygame.transform.scale(load_image('wN.png'), (80, 80)),
    'bishop': pygame.transform.scale(load_image('wB.png'), (80, 80)),
    'queen': pygame.transform.scale(load_image('wQ.png'), (80, 80)),
    'king': pygame.transform.scale(load_image('wK.png'), (80, 80)),
}

<<<<<<< HEAD
=======
pygame.init()
screen = pygame.display.set_mode((800, 800)) # Set the dimensions of the screen
pygame.display.set_caption('Chess') # Set the title of the window
clock = pygame.time.Clock() # Create a clock object to control the frame rate
running = True # A variable to control the game loop

>>>>>>> 3e3cddac1aa285f93849be2610b26b0887faa174
def draw_chess_board():
    pygame.draw.rect(screen, DARK_SQUARE, [0, 0, 800, 800])
    pygame.draw.line(screen, 'black', (801, 0), (801, 800), 4)
    pygame.draw.line(screen, 'black', (0, 801), (800, 801), 4)

    for i in range(8):
        for j in range(8):
            square_rect = pygame.Rect(j * 100, i * 100, 100, 100)
            pygame.draw.rect(screen, GRID_COLOR, square_rect, 1)
            pygame.draw.rect(screen, LIGHT_SQUARE if (i + j) % 2 == 0 else DARK_SQUARE, square_rect)

    pygame.draw.rect(screen, DARK_SQUARE, [0, 800, 800, 100])
    pygame.draw.rect(screen, DARK_SQUARE, [800, 0, 200, 800])

piece_state = {}
def draw_pieces():
    for name, row, col in black_location:
        piece = name[:-2]  # Extract piece type from name
        image = black_pieces_images.get(f'{piece.lower()}')  # Convert to lowercase
        if image:
            x = int(col * 100 + 10)
            y = int(row * 100 + 10)
            screen.blit(image, (x, y))

    for name, row, col in white_location:
        piece = name[:-2]  # Extract piece type from name
        image = white_pieces_images.get(f'{piece.lower()}')  # Convert to lowercase
        if image:
            x = int(col * 100 + 10)
            y = int(row * 100 + 10)
            screen.blit(image, (x, y))

            # Display state text on the pieces
            piece_key = (row, col, piece.lower())
            if piece_key in piece_state:
                font = pygame.font.Font(None, 20)
                text = font.render(piece_state[piece_key], True, (255, 255, 255))
                screen.blit(text, (x + 20, y + 60))

def is_valid_pawn_move(start, end, color):
    row_start, col_start = start
    row_end, col_end = end

    if color == 'white':
        # White pawn moves forward one square
        return row_end == row_start - 1 and col_end == col_start
    elif color == 'black':
        # Black pawn moves forward one square
        return row_end == row_start + 1 and col_end == col_start

    return False

def is_valid_rook_move(start, end):
    row_start, col_start = start
    row_end, col_end = end

    # Rook moves horizontally or vertically
    return row_start == row_end or col_start == col_end

def is_valid_knight_move(start, end):
    row_diff = abs(end[0] - start[0])
    col_diff = abs(end[1] - start[1])

    # Knight moves in an L-shape
    return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

def is_valid_bishop_move(start, end):
    row_diff = abs(end[0] - start[0])
    col_diff = abs(end[1] - start[1])

    # Bishop moves diagonally
    return row_diff == col_diff

def is_valid_queen_move(start, end):
    row_start, col_start = start
    row_diff = abs(end[0] - row_start)
    col_diff = abs(end[1] - col_start)

    # Queen combines rook and bishop moves
    return (row_start == end[0] or col_start == end[1]) or (row_diff == col_diff)

def is_valid_king_move(start, end):
    row_diff = abs(end[0] - start[0])
    col_diff = abs(end[1] - start[1])

    # King moves one square in any direction
    return row_diff <= 1 and col_diff <= 1

while running:
    clock.tick(60)
    screen.fill((255, 255, 255))
    draw_chess_board()
    draw_pieces()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


############################################################################################################
# Example usage for pawn
start_position = (6, 3)
end_position = (6, 4)  # Intentionally incorrect move
piece_type = 'pawn'
color = 'white'

if is_valid_pawn_move(start_position, end_position, color):
    print(f"Valid move for {color} {piece_type}")
else:
    print(f"Invalid move for {color} {piece_type}")

# Example usage for knight
start_position = (7, 6)
end_position = (5, 6)  # Intentionally incorrect move
piece_type = 'knight'

if is_valid_knight_move(start_position, end_position):
    print(f"Valid move for {color} {piece_type}")
else:
    print(f"Invalid move for {color} {piece_type}")

# Example usage for rook
start_position = (0, 0)
end_position = (2, 0)
piece_type = 'rook'

if is_valid_rook_move(start_position, end_position):
    print(f"Valid move for {color} {piece_type}")
else:
    print(f"Invalid move for {color} {piece_type}")

# Example usage for knight
start_position = (7, 6)
end_position = (5, 5)
piece_type = 'knight'

if is_valid_knight_move(start_position, end_position):
    print(f"Valid move for {color} {piece_type}")
else:
    print(f"Invalid move for {color} {piece_type}")

# Example usage for bishop
start_position = (2, 0)
end_position = (0, 2)
piece_type = 'bishop'

if is_valid_bishop_move(start_position, end_position):
    print(f"Valid move for {color} {piece_type}")
else:
    print(f"Invalid move for {color} {piece_type}")

# Example usage for queen
start_position = (0, 3)
end_position = (3, 0)
piece_type = 'queen'

if is_valid_queen_move(start_position, end_position):
    print(f"Valid move for {color} {piece_type}")
else:
    print(f"Invalid move for {color} {piece_type}")

# Example usage for king
start_position = (0, 4)
end_position = (1, 3)
piece_type = 'king'

if is_valid_king_move(start_position, end_position):
    print(f"Valid move for {color} {piece_type}")
else:
    print(f"Invalid move for {color} {piece_type}")


############################################################################################################


pygame.quit()
sys.exit()

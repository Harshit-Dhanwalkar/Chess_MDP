#Ganesh was here
#Harshit was here
import pygame
import sys

pygame.init()
pygame.display.set_caption('Chess')
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
running = Truerotate
LIGHT_SQUARE = (245, 203, 167)  # LIGHT SQUARES
DARK_SQUARE = (87, 65, 18)  # DARK SQUARES
GRID_COLOR = (0, 0, 0)  # GRID COLOR

turn_step = 0
selection = 100
valid_moves = []

# Add a variable to store the highlighted square position
highlighted_square = None

# Add a variable to store the valid moves for the selected piece
selected_valid_moves = []

# Assuming these are your piece lists
black_pieces = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'rook', 'rook', 'knight', 'knight',
                'bishop', 'bishop', 'queen', 'king']
white_pieces = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'rook', 'rook', 'knight', 'knight',
                'bishop', 'bishop', 'queen', 'king']

# Assuming these are your initial piece positions
black_location = [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [0, 0], [0, 7], [0, 1], [0, 6], [0, 2],
                  [0, 5], [0, 3], [0, 4]]
white_location = [[6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7], [7, 0], [7, 7], [7, 1], [7, 6], [7, 2],
                  [7, 5], [7, 3], [7, 4]]

captured_piece_black = []

IMAGE_PATH = r'C:\Users\harsh\OneDrive\Desktop\PYTHONsmallprojects\Chess\Pieces_PNG\svgtopng'

# Load images for pieces
black_pieces_images = {
    'pawn': pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}\\bP.png'), (80, 80)),
    'rook': pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}\\bR.png'), (80, 80)),
    'knight': pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}\\bN.png'), (80, 80)),
    'bishop': pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}\\bB.png'), (80, 80)),
    'queen': pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}\\bQ.png'), (80, 80)),
    'king': pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}\\bK.png'), (80, 80)),
}

white_pieces_images = {
    'pawn': pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}\\wP.png'), (80, 80)),
    'rook': pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}\\wR.png'), (80, 80)),
    'knight': pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}\\wN.png'), (80, 80)),
    'bishop': pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}\\wB.png'), (80, 80)),
    'queen': pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}\\wQ.png'), (80, 80)),
    'king': pygame.transform.scale(pygame.image.load(f'{IMAGE_PATH}\\wK.png'), (80, 80)),
}

# Add a dictionary to store the state of each piece
# Key format: (row, column, piece_type)
piece_state = {}

def draw_chess_board():
    pygame.draw.rect(screen, DARK_SQUARE, [0, 0, 800, 800])
    pygame.draw.line(screen, 'black', (801, 0), (801, 800), 4)
    pygame.draw.line(screen, 'black', (0, 801), (800, 801), 4)
    for i in range(8):
        for j in range(8):
            square_rect = pygame.Rect(j * 100, i * 100, 100, 100)
            pygame.draw.rect(screen, GRID_COLOR, square_rect, 1)  # Add this line to draw the border

            # Highlight the square with a red border if it matches the selected piece
            if highlighted_square and square_rect.collidepoint(highlighted_square):
                pygame.draw.rect(screen, (255, 0, 0), square_rect, 5)
            else:
                pygame.draw.rect(screen, LIGHT_SQUARE if (i + j) % 2 == 0 else DARK_SQUARE, square_rect)

    pygame.draw.rect(screen, DARK_SQUARE, [0, 800, 800, 100])
    pygame.draw.rect(screen, DARK_SQUARE, [800, 0, 200, 800])

    status_text = ['White to move', 'Black to move', 'White wins', 'Black wins', 'Stalemate', 'Checkmate', 'Draw']

    if turn_step == 0:
        font = pygame.font.Font(None, 36)  # adjust the font size
        text = font.render(status_text[turn_step], True, (255, 255, 255))
        screen.blit(text, (810, 50))

    elif turn_step == 1:
        font = pygame.font.Font(None, 36)
        text = font.render(status_text[turn_step], True, (255, 255, 255))
        screen.blit(text, (810, 50))

    elif turn_step == 2:
        text = pygame.font.Font(None, 36).render(status_text[turn_step], True, 'black')
        screen.blit(text, (810, 50))
    elif turn_step == 3:
        text = pygame.font.Font(None, 36).render(status_text[turn_step], True, 'black')
        screen.blit(text, (810, 50))

    for i in range(8):
        pygame.draw.line(screen, 'black', (i * 100, 0), (i * 100, 800), 2)
        pygame.draw.line(screen, 'black', (0, i * 100), (800, i * 100), 2)

def highlight_square(screen, position, color):
    rect = pygame.Rect(position[1] * 100, position[0] * 100, 100, 100)
    pygame.draw.rect(screen, color, rect, 5)

def draw_valid_moves(screen, valid_moves, color):
    for move in valid_moves:
        rect = pygame.Rect(move[1] * 100, move[0] * 100, 100, 100)
        pygame.draw.rect(screen, color, rect, 5)

# draw chess pieces
def draw_pieces():
    for piece, position in zip(black_pieces, black_location):
        image = black_pieces_images[f'{piece.lower()}']
        screen.blit(image, (position[1] * 100 + 10, position[0] * 100 + 10))

    for piece, position in zip(white_pieces, white_location):
        image = white_pieces_images[f'{piece.lower()}']
        screen.blit(image, (position[1] * 100 + 10, position[0] * 100 + 10))

        # Display state text on the pieces
        piece_key = (position[0], position[1], piece.lower())
        if piece_key in piece_state:
            font = pygame.font.Font(None, 20)
            text = font.render(piece_state[piece_key], True, (255, 255, 255))
            screen.blit(text, (position[1] * 100 + 30, position[0] * 100 + 70))

# draw valid moves
def check_options(pieces, location, turn):
    valid_moves = []
    for i in range(len(pieces)):
        piece_color = 'white' if turn == 0 else 'black'
        opponent_color = 'black' if turn == 0 else 'white'

        if pieces[i] == 'pawn':
            forward_dir = -1 if piece_color == 'white' else 1

            # Check one square forward
            if [location[i][0] + forward_dir, location[i][1]] not in location:
                valid_moves.append([location[i][0] + forward_dir, location[i][1]])

            # Check two squares forward if it's the pawn's first move
            if (
                location[i][0] == 6 and piece_color == 'white'
            ) or (
                location[i][0] == 1 and piece_color == 'black'
            ):
                if [location[i][0] + 2 * forward_dir, location[i][1]] not in location:
                    valid_moves.append([location[i][0] + 2 * forward_dir, location[i][1]])

            # Check diagonal captures
            if [location[i][0] + forward_dir, location[i][1] - 1] in location and piece_color != opponent_color:
                valid_moves.append([location[i][0] + forward_dir, location[i][1] - 1])
            if [location[i][0] + forward_dir, location[i][1] + 1] in location and piece_color != opponent_color:
                valid_moves.append([location[i][0] + forward_dir, location[i][1] + 1])

            # Add state for pawn
            piece_key = (location[i][0], location[i][1], 'pawn')
            if (
                (location[i][0] == 6 and piece_color == 'white')
                or (location[i][0] == 1 and piece_color == 'black')
            ) and piece_key not in piece_state:
                piece_state[piece_key] = "Not Moved"
            elif piece_key in piece_state:
                piece_state[piece_key] = "Moved"

    return valid_moves


fps = 60
while running:
    clock.tick(fps)
    screen.fill('white')
    draw_chess_board()

    # Draw pieces after drawing the chessboard
    draw_pieces()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            click_coords = event.pos

            # Check if the clicked position is on a piece
            if turn_step == 0:
                for piece_position in white_location:
                    piece_rect = pygame.Rect(piece_position[1] * 100, piece_position[0] * 100, 100, 100)

                    if piece_rect.collidepoint(click_coords):
                        # Highlight the square of the clicked piece
                        highlighted_square = (piece_position[0], piece_position[1])

                        # Get valid moves for the selected piece
                        selected_valid_moves = check_options(white_pieces, white_location, 0)
                        break  # Break to avoid highlighting multiple squares if pieces overlap

            elif turn_step == 1:
                for piece_position in black_location:
                    piece_rect = pygame.Rect(piece_position[1] * 100, piece_position[0] * 100, 100, 100)

                    if piece_rect.collidepoint(click_coords):
                        # Highlight the square of the clicked piece
                        highlighted_square = (piece_position[0], piece_position[1])

                        # Get valid moves for the selected piece
                        selected_valid_moves = check_options(black_pieces, black_location, 1)
                        break  # Break to avoid highlighting multiple squares if pieces overlap
            else:
                # Reset the highlighted square and valid moves if the click is not on any piece
                highlighted_square = None
                selected_valid_moves = []

        if event.type == pygame.MOUSEBUTTONUP:
            release_coords = event.pos

            # Check if the release position is within the chessboard
            if 0 <= release_coords[0] < 800 and 0 <= release_coords[1] < 800:
                # Calculate the row and column of the released position
                row = release_coords[1] // 100
                col = release_coords[0] // 100

                # Check if the release position is a valid move
                if [row, col] in selected_valid_moves:
                    # Update the position of the selected piece
                    if turn_step == 0:
                        try:
                            piece_index = white_location.index([highlighted_square[0], highlighted_square[1]])
                            white_location[piece_index] = [row, col]
                        except ValueError:
                            # Handle the case where the position is not found in white_location
                            print(f"Error: Selected piece {highlighted_square} not found in white_location")
                            print("Current white_location:", white_location)
                    elif turn_step == 1:
                        try:
                            piece_index = black_location.index([highlighted_square[0], highlighted_square[1]])
                            black_location[piece_index] = [row, col]
                        except ValueError:
                            # Handle the case where the position is not found in black_location
                            print(f"Error: Selected piece {highlighted_square} not found in black_location")
                            print("Current black_location:", black_location)

                    # Reset the highlighted square and valid moves after placing the piece
                    highlighted_square = None
                    selected_valid_moves = []

    # Highlight the selected piece square
    if highlighted_square:
        highlight_square(screen, highlighted_square, (255, 0, 0))

    # Highlight valid moves
    draw_valid_moves(screen, selected_valid_moves, (0, 255, 0))

    pygame.display.flip()

pygame.quit()
sys.exit()

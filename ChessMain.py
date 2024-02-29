# Ganesh was here
# Harshit was here 
# Updated by: Harshit


'''
Used to main driver file to run the chess game and handling your input and displaying the current Gamestate
'''

import pygame as p
from ChessEngine import GameState
from ChessEngine import Move
import pygame as p

WIDTH = HEIGHT = 620 #512 #400
DIMENSION = 8 #8 for a chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animations
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''
def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("./images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        # Note: we can access an image by saying 'IMAGES['wp']'

'''
The main driver for our code. This will handle user input and updating the graphics
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made
    # print(gs.board)
    loadImages() # only do this once, before the while loop
    running = True
    sqSelected = () # no square is selected initially, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                print(gs.moveLog)
                print("Game Over")
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): # the user clicked the same square twice
                   sqSelected = () # deselect
                   playerClicks = [] # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # append for both 1st and 2nd clicks
        if len(playerClicks) == 2:  # after 2nd click
            move = Move(playerClicks[0], playerClicks[1], gs.board)
            print(move.getChessNotation())
            if move in validMoves:  # Check if the move is valid
                gs.makeMove(move)
                moveMade = True
                sqSelected = ()  # reset user clicks
                playerClicks = []
            else:
                playerClicks = [sqSelected]

        # key handler
        elif e.type == p.KEYDOWN:
            if e.key == p.K_z: # undo when 'z' is pressed
                gs.undoMove()
                moveMade = True

        if moveMade:
            #gs.changeTurn()  # Make sure to change turn after a move
            validMoves = gs.getValidMoves()
            moveMade = False         

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsible for all the graphics within a current game state.
'''
def drawGameState(screen, gs):
    drawBoard(screen) # draw squares on the board
    # add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board) # draw pieces on top of those squares

'''
Draw the squares on the board. The top left square is always light.
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the pieces on the board using the current GameState's board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
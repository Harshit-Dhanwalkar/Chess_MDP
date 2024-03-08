import chess
import chess.svg
import math
import base64
from PIL import Image 
from cairosvg import svg2png


def eval_func(x):
    return math.sin(x) # We are taking J(x) = sin(x)

def encode_board(board):
    # Encode the board using base64
    encoded_board = base64.b64encode(board.board_fen().encode('utf-8')).decode('utf-8')
    return encoded_board

def decode_board(encoded_board):
    # Decode the encoded board using base64
    decoded_board_fen = base64.b64decode(encoded_board.encode('utf-8')).decode('utf-8')
    board = chess.Board(decoded_board_fen)
    return board

def base64_to_int(encoded_board):
    bytes_repr = base64.b64decode(encoded_board)
    int_repr = int.from_bytes(bytes_repr, 'big')
    return int_repr

def showBoard(board):
    f = open("pic.svg","w")
    a = chess.svg.board(board)
    f.write(a)
    f.close()
    svg2png(url="./pic.svg", write_to="./pic.png")
    im = Image.open("pic.png")
    im.show()

def simple_terminal_engine():
    # Create a chess board
    board = chess.Board()

    while not (board.is_checkmate() and board.is_stalemate() and board.is_insufficient_material()):
        #curr_eval = eval_func(base64_to_int(encode_board(board)))
        final_eval_arr = []
        A = [i for i in board.legal_moves]
        for WhiteMove in A:
            board.push_san(str(WhiteMove))
            temp = []
            for BlackMove in board.legal_moves:
                board.push_san(str(BlackMove))
                intermediate_eval = eval_func(base64_to_int(encode_board(board)))
                temp.append(intermediate_eval)
                board.pop()
            final_eval_arr.append(min(temp))
            board.pop()
        final_eval = max(final_eval_arr)
        action = final_eval_arr.index(final_eval)
        board.push_san(str(A[action]))
        print(board)
        showBoard(board)
        PlayerMove = str(input("Enter move : "))
        board.push_san(PlayerMove)
        print(board)
        showBoard(board)
simple_terminal_engine()


        
        



                
            


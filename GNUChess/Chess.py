import chess
import chess.svg
import math
import base64
import cv2
from cairosvg import svg2png


def eval_func(x):
    return math.cos(x)  # We are taking J(x) = exponential function


def encode_board(board):
    # Encode the board using base64
    encoded_board = base64.b64encode(board.board_fen().encode("utf-8")).decode("utf-8")
    return encoded_board


def decode_board(encoded_board):
    # Decode the encoded board using base64
    decoded_board_fen = base64.b64decode(encoded_board.encode("utf-8")).decode("utf-8")
    board = chess.Board(decoded_board_fen)
    return board


def base64_to_int(encoded_board):
    bytes_repr = base64.b64decode(encoded_board)
    int_repr = int.from_bytes(bytes_repr, "big")
    return int_repr


def dispBoard(board):
    f = open("pic.svg", "w")
    a = chess.svg.board(board, flipped=True)
    f.write(a)
    f.close()
    svg2png(url="./pic.svg", write_to="./pic.png")
    image = cv2.imread("./pic.png")
    cv2.imshow("image window", image)
    # cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()


def simple_terminal_engine():
    # Create a chess board
    board = chess.Board()
    state_list = [board]

    while True:
        final_eval_arr = []
        A = [i for i in board.legal_moves]  # Creating action space
        for WhiteMove in A:
            board.push_san(
                str(WhiteMove)
            )  # This function plays the move and modifies board
            temp = []
            for BlackMove in board.legal_moves:
                board.push_san(str(BlackMove))
                intermediate_eval = eval_func(base64_to_int(encode_board(board)))
                temp.append(intermediate_eval)
                board.pop()  # Undo the last move
            final_eval_arr.append(min(temp))
            board.pop()
        final_eval = max(final_eval_arr)
        action = final_eval_arr.index(final_eval)
        board.push_san(str(A[action]))
        print(board)
        dispBoard(board)
        if board.is_checkmate():
            state_list.append("W")
            break
        if board.is_insufficient_material():
            state_list.append("D")
            break
        while True:
            try:
                PlayerMove = str(input("Enter move : "))
                board.push_san(PlayerMove)
                state_list.append(board)
                break
            except ValueError:
                print("Invalid move. Please try again.")
                board.pop()
        print(board)
        dispBoard(board)
        if board.is_checkmate():
            state_list.append("L")
            break
        if board.is_insufficient_material():
            state_list.append("D")
            break

    return state_list


l = simple_terminal_engine()

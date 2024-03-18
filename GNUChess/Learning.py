import chess
import chess.engine
import chess.svg
import math
import base64
import cv2
from cairosvg import svg2png
from scipy.optimize import fsolve


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
    engine = chess.engine.SimpleEngine.popen_uci(r"stockfish")
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
                intermediate_eval = func(base64_to_int(encode_board(board)))
                temp.append(intermediate_eval)
                board.pop()  # Undo the last move
            final_eval_arr.append(min(temp))
            board.pop()
        final_eval = max(final_eval_arr)
        action = final_eval_arr.index(final_eval)
        board.push_san(str(A[action]))
        print("Engine move : ", A[action])
        print(board)
        dispBoard(board)
        if board.is_checkmate():
            state_list.append("W")
            break
        if board.is_insufficient_material():
            state_list.append("D")
            break
        #while True:
        #    try:
        #        PlayerMove = str(input("Enter move : "))
        #        board.push_san(PlayerMove)
        #        state_list.append(board)
        #        break
        #    except ValueError:
        #        print("Invalid move. Please try again.")
        stock_move = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(stock_move.move)
        print(board)
        dispBoard(board)
        if board.is_checkmate():
            state_list.append("L")
            break
        if board.is_insufficient_material():
            state_list.append("D")
            break

    return state_list


A = float(input("A = "))
B = float(input("B = "))
C = float(input("C = "))
D = float(input("D = "))


def func(x):
    return (
        A * math.sin(x) + B * math.cos(x) + C * math.atan(x) + D * math.tanh(x) 
    )


def func_deriv(x):  # derivative of func(x)
    return (
        A * math.cos(x)
        - B * math.sin(x)
        + C * (1 / (1 + (x**2)))
        + D * (1/math.cosh(x))**2
    )


def compute_max():
    guess = []
    for i in range(0, 100, 10):
        try:
            temp = fsolve(func_deriv, i)
            guess.append(func(temp))
        except:
            break
    return max(guess)


def sum_from(arr, t):  # This is out $\Delta t$
    n = len(arr)
    sum = 0
    lamb = 0.7
    for i in range(t, n):
        sum += (lamb ** (i - t)) * arr[i]
    return sum


def grad(x, max):
    return [math.sin(x)/max, math.cos(x)/max, math.atan(x)/max, math.tanh(x)/max]


def engine_learn():
    state_list = simple_terminal_engine()
    N = len(state_list) - 1  # Actual length of the game neglecting the final element
    rN = 0
    if state_list[N] == "W":
        rN = 1
    elif state_list[N] == "L":
        rN = -1
    d = []  # Temporal differences are stored here
    max_func = compute_max()
    for t in range(0, N - 1):
        J_t = func(base64_to_int(encode_board(state_list[t]))) / max_func
        if J_t > 1:
            J_t = 0.99
        J_tp = func(base64_to_int(encode_board(state_list[t + 1]))) / max_func
        if J_tp > 1:
            J_tp = 0.99
        d.append(J_tp - J_t)
    J = func(base64_to_int(encode_board(state_list[N - 1]))) / max_func
    if J > 1:
        J = 0.99
    temp = rN - J
    d.append(temp)
    update = [A, B, C, D]  # This will contain the corrected coefficients
    for t in range(N):
        x = base64_to_int(encode_board(state_list[t]))
        temp = grad(x, max_func)  # The gradient at a particular state
        delta_t = sum_from(d, t)  # This is our $\Delta t$
        for i in range(len(temp)):
            update[i] += temp[i] * delta_t
    return update

while True:
    l = engine_learn()  
    A = l[0]
    B = l[1]
    C = l[2]
    D = l[3]
    f = open("Parameters.txt", "a")
    text = str(l) + '\n'
    f.write(text)
    f.close()
    print(l)


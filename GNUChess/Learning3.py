import chess
import chess.engine
import chess.svg
import cv2
import numpy as np
from cairosvg import svg2png

A = float(input("A = "))
B = float(input("B = "))
n = int(input("Number of games = "))
depth = int(input("depth = "))
man = bool(input("MANUAL = "))

# Precompute square values for piece placement evaluation
square_values = {
    chess.E5: 2, chess.E4: 2, chess.D5: 2, chess.D4: 2,
    chess.F6: 1, chess.E6: 1, chess.D6: 1, chess.C6: 1,
    chess.F3: 1, chess.E3: 1, chess.D3: 1, chess.C3: 1,
    chess.F5: 1, chess.F4: 1, chess.C5: 1, chess.C4: 1,
}

def material(board):
    value = {
        "p": -1, "b": -3, "n": -3, "r": -5, "q": -9,
        "P": 1, "B": 3, "N": 3, "R": 5, "Q": 9,
    }
    temp = board.fen()
    ret = 0
    for c in temp:
        try:
            ret += value[c]
        except:
            continue
    return ret

def cent_cont(board):
    ret = 0
    for square, val in square_values.items():
        white_attackers = len(board.attackers(chess.WHITE, square))
        black_attackers = len(board.attackers(chess.BLACK, square))
        ret += (white_attackers - black_attackers) * val
    return ret

def ev_func(board):
    return A * material(board) + B * cent_cont(board)

def dispBoard(board):
    f = open("pic.svg", "w")
    a = chess.svg.board(board, flipped=man)
    f.write(a)
    f.close()
    svg2png(url="./pic.svg", write_to="./pic.png")
    image = cv2.imread("./pic.png")
    cv2.imshow("image window", image)
    cv2.waitKey(1)  # Wait for a short duration to display image

def generateMove(board, count=1):
    if count == depth:
        final_eval_arr = []
        for whiteMove in board.legal_moves:
            board.push_san(str(whiteMove))
            black_eval = []
            for blackMove in board.legal_moves:
                board.push_san(str(blackMove))
                intermediate_eval = ev_func(board)
                black_eval.append(intermediate_eval)
                board.pop()
            final_eval_arr.append(min(black_eval))
            board.pop()
        final_eval = max(final_eval_arr)
        action_ind = final_eval_arr.index(final_eval)
        return [list(board.legal_moves)[action_ind], final_eval]

    final_eval_arr = []h
    for whiteMove in board.legal_moves:
        board.push_san(str(whiteMove))
        final_eval = -np.inf
        for blackMove in board.legal_moves:
            board.push_san(str(blackMove))
            temp = generateMove(board, count + 1)
            final_eval = max(final_eval, temp[1])
            board.pop()
        final_eval_arr.append(final_eval)
        board.pop()
    best_move_index = np.argmax(final_eval_arr)
    return [list(board.legal_moves)[best_move_index], final_eval_arr[best_move_index]]

def simple_terminal_engine():
    board = chess.Board()
    state_list = [board]
    engine = chess.engine.SimpleEngine.popen_uci(r"stockfish")
    while True:
        action = generateMove(board)
        board.push_san(str(action[0]))
        print("Engine move : ", action[0])
        print(board)
        dispBoard(board)
        if board.is_game_over():
            state_list.append(board.result())
            break
        if man:
            while True:
                try:
                    PlayerMove = str(input("Enter move : "))
                    board.push_san(PlayerMove)
                    state_list.append(board)
                    break
                except ValueError:
                    print("Invalid move. Please try again.")
        else:
            stock_move = engine.play(board, chess.engine.Limit(time=0.1))
            board.push(stock_move.move)
            state_list.append(board)
        print(board)
        dispBoard(board)
        if board.is_game_over():
            state_list.append(board.result())
            break
    engine.quit()
    return state_list

def sum_from(arr, t):
    return sum(arr[t:])

def grad(state):    # Gradient of the evaluation function
    return [material(state), cent_cont(state)]

def engine_learn(a):
    state_list = simple_terminal_engine()
    N = len(state_list) - 1  # Actual length of the game neglecting the final element
    rN = 0
    if state_list[N] == "1-0":
        print("White won!")
        rN = 100 * (A + B)
    elif state_list[N] == "0-1":
        print("Black won!")
        rN = -100 * (A + B)

    d = []  # Temporal differences are stored here
    for t in range(0, N - 1):
        J_t = ev_func(state_list[t])
        J_tp = ev_func(state_list[t + 1])
        d.append(J_tp - J_t)
    J = ev_func(state_list[N - 1])
    d.append(rN - J)
    update = [A, B]  # This will contain the corrected coefficients
    for t in range(N):
        temp = grad(state_list[t])  # The gradient at a particular state
        delta_t = sum_from(d, t)  # This is our $\Delta t$
        for i in range(len(temp)):
            update[i] += temp[i] * delta_t * a
    return update

# Main loop for learning
while n > 0:
    l = engine_learn(n)
    A = l[0]
    B = l[1]
    with open("Parameters3.txt", "a") as f:
        text = str(l) + "\n"
        f.write(text)
    print(l)
    n -= 1


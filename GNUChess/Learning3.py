import chess
import chess.engine
import chess.svg
import cv2
from cairosvg import svg2png
import os 
from multiprocessing import Pool

A = float(input("A (coeff. of material) = "))
B = float(input("B (coeff. of central control) = "))
C = float(input("C (coeff. of pawn structure) = "))
D = float(input("D (coeff. of black king safety) = "))
E = float(input("E (coeff. of white king safety) = "))

n = int(input("Number of games = "))
depth = int(input("depth (no. of turns you want algorithm to think furthur) = "))
man = bool(input("MANUAL (leave it blank if you want automation) = "))

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
    # Evaluate the control of the center
    ret = 0
    for square, val in square_values.items():
        white_attackers = len(board.attackers(chess.WHITE, square))
        black_attackers = len(board.attackers(chess.BLACK, square))
        ret += (white_attackers - black_attackers) * val
    return ret

def pawn_structure(board):
    # Evaluate the pawn structure
    white_pawns = board.pieces(chess.PAWN, chess.WHITE)
    black_pawns = board.pieces(chess.PAWN, chess.BLACK)
    white_pawn_structure = 0
    black_pawn_structure = 0

    for square in white_pawns:
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        if file == 0 or file == 7:
            white_pawn_structure -= 1
        if rank == 1:
            white_pawn_structure -= 1
        if rank == 6:
            white_pawn_structure += 1

    for square in black_pawns:
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        if file == 0 or file == 7:
            black_pawn_structure -= 1
        if rank == 1:
            black_pawn_structure += 1
        if rank == 6:
            black_pawn_structure -= 1

    return white_pawn_structure + black_pawn_structure



def black_king_safety(board):
    # Evaluate the safety of the black king
    king_square = board.king(chess.BLACK)  # finds the position of Black king on board
    attackers = board.attackers(chess.WHITE, king_square)
    return -len(attackers)   # -ve sign means more the attackers less the safety

def white_king_safety(board):
    # Evaluate the safety of the white king
    king_square = board.king(chess.WHITE)
    attackers = board.attackers(chess.BLACK, king_square)
    return -len(attackers)

'''
def black_king_safety(board):
    # Evaluate the safety of the black king and surrounding squares
    king_square = board.king(chess.BLACK)
    surrounding_squares = []

    # Iterate over surrounding squares and add valid ones to the list
    for file_offset in [-1, 0, 1]:
        for rank_offset in [-1, 0, 1]:
            square = chess.square(chess.square_file(king_square) + file_offset, chess.square_rank(king_square) + rank_offset)
            if chess.square_file(square) in range(8) and chess.square_rank(square) in range(8):
                surrounding_squares.append(square)

    return -len(board.attackers(chess.WHITE, king_square)) - len(board.attackers(chess.WHITE, surrounding_squares))

def white_king_safety(board):
    # Evaluate the safety of the white king and surrounding squares
    king_square = board.king(chess.WHITE)
    surrounding_squares = []

    # Iterate over surrounding squares and add valid ones to the list
    for file_offset in [-1, 0, 1]:
        for rank_offset in [-1, 0, 1]:
            square = chess.square(chess.square_file(king_square) + file_offset, chess.square_rank(king_square) + rank_offset)
            if chess.square_file(square) in range(8) and chess.square_rank(square) in range(8):
                surrounding_squares.append(square)

    return -len(board.attackers(chess.BLACK, king_square)) - len(board.attackers(chess.BLACK, surrounding_squares))
'''

def ev_func(board):
    return A * material(board) + B * cent_cont(board) + C * pawn_structure(board) + D * black_king_safety(board) + E * white_king_safety(board)

def dispBoard(board):
    f = open("pic.svg", "w")
    a = chess.svg.board(board, flipped=man)
    f.write(a)
    f.close()
    svg2png(url="./pic.svg", write_to="./pic.png")
    image = cv2.imread("./pic.png")
    cv2.imshow("image window", image)
    cv2.waitKey(1)  # Wait for a short duration to display image

def generateReward(board, move, count=1):  # returns eval
    brd = board.copy()
    if count == depth:
        brd.push_san(str(move))
        temp = []
        print("BLACK LOOP 1")
        for BlackMove in brd.legal_moves:
            brd.push_san(str(BlackMove))
            temp.append(ev_func(brd))
            brd.pop()
        brd.pop()
        print(temp)
        if temp:
            return min(temp)
        else:
            return float('inf')  # Return a default value if temp is empty

    else:
        brd.push_san(str(move))
        black_eval = []
        for BlackMove in brd.legal_moves:
            brd.push_san(str(BlackMove))
            white_eval = []
            # print("-------------------------------------")
            for WhiteMove in brd.legal_moves:
                print("WHITE LOOP 2")
                white_eval.append(generateReward(brd, WhiteMove, count + 1))
            black_eval.append(max(white_eval))
            brd.pop()
        brd.pop()
        print(black_eval)
        if black_eval:
            return min(black_eval)
        else:
            return -float('inf')  # Return a default value if black_eval is empty


def simple_terminal_engine():
    # Create a chess board
    board = chess.Board()
    state_list = [board]
    engine = chess.engine.SimpleEngine.popen_uci(r"stockfish")
    while True:
        #action = generateMove(board)
        #board.push_san(str(action[0]))
        #print("Engine move : ", action[0])
        
        A = [(board, move) for move in board.legal_moves]
        rewards = []
        with Pool(os.cpu_count()) as p:
            rewards = p.starmap(generateReward, A)

        max_eval = max(rewards) 
        bestMove = A[rewards.index(max_eval)][1]
        print("Engine move : ", bestMove)
        board.push_san(str(bestMove))
        print(board)
        dispBoard(board)
        if board.is_checkmate():
            state_list.append("W")
            break
        if board.is_insufficient_material():
            state_list.append("D")
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
        if board.is_checkmate():
            state_list.append("L")
            break
        if board.is_insufficient_material():
            state_list.append("D")
            break
    engine.quit()
    return state_list


def sum_from(arr, t):
    return sum(arr[t:])

def grad(state):    # Gradient of the evaluation function
    return [material(state), cent_cont(state), pawn_structure(state), black_king_safety(state) ,white_king_safety(state)]

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
    update = [A, B, C, D, E]  # This will contain the corrected coefficients
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
    C = l[2]
    D = l[3]
    E = l[4]
    with open("Parameters3.txt", "a") as f:
        text = str(l) + "\n"
        f.write(text)
    print(l)
    n -= 1

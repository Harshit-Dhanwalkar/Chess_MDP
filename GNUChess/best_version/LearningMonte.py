#! /bin/python3
import chess
import chess.engine
import chess.svg
import cv2
from cairosvg import svg2png
from multiprocessing import Pool
import os

A = float(input("A (coeff. of material) = "))
B = float(input("B (coeff. of central control) = "))
C = float(input("C (coeff. of king safety) = "))
D = float(input("D (coeff. of mobility) = "))


n = int(input("Number of games = "))
depth = int(input("depth (no. of turns you want algorithm to think furthur) = "))
man = bool(input("MANUAL (leave it blank if you want automation) = "))

class node:
    def __init__(self, board, parent):
        self.board = board
        self.eval = ev_func(board)
        self.parent = parent 
        self.children = []

        


def dispBoard(board):
    # Function to display the board
    f = open("pic.svg", "w")
    a = chess.svg.board(board, flipped=man)
    f.write(a)
    f.close()
    svg2png(url="./pic.svg", write_to="./pic.png")
    image = cv2.imread("./pic.png")
    cv2.imshow("image window", image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()


def material(board):
    # Assign value to the pieces
    value = {
        "p": -1,
        "b": -3,
        "n": -3,
        "r": -5,
        "q": -9,
        "P": 1,
        "B": 3,
        "N": 3,
        "R": 5,
        "Q": 9,
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
    value = {
        chess.E5: 2,
        chess.E4: 2,
        chess.D5: 2,
        chess.D4: 2,
        chess.F6: 1,
        chess.E6: 1,
        chess.D6: 1,
        chess.C6: 1,
        chess.F3: 1,
        chess.E3: 1,
        chess.D3: 1,
        chess.C3: 1,
        chess.F5: 1,
        chess.F4: 1,
        chess.C5: 1,
        chess.C4: 1,
    }
    ret = 0
    for square in value.keys():
        whiteAttackers = len(board.attackers(chess.WHITE, square)) # Number of white pieces controlling the centre. 
        blackAttackers = len(board.attackers(chess.BLACK, square))# Number of black pieces controlling the centre.
        ret += (whiteAttackers - blackAttackers) * value[square]
    return ret

def kingSafety(board):
    surrounding = [[7,8,9],[-1,0,1],[-9, -8, -7]]
    white_king_index = board.king(chess.WHITE)
    black_king_index = board.king(chess.BLACK)
    ret = 0
    for i in range(0,3):
        for j in range(0,3):
            try:
                blackAttackers = len(board.attackers(chess.BLACK, white_king_index + surrounding[i][j])) # Number of attackers near white king
                whiteAttackers = len(board.attackers(chess.WHITE,  black_king_index + surrounding[i][j]))#  Number of attackers near black king
                ret += (whiteAttackers - blackAttackers)
            except IndexError:
                continue
    return ret

def mobiltity(board):
    temp = [i for i in board.legal_moves]
    return len(temp)

def gameOver(board):
    if(board.is_checkmate()):
        outcome = board.outcome()
        if(outcome.winner == chess.WHITE):
            return 100000*(A + B + C + D)
        else:
            return -100000*(A + B + C + D)
    else:
        return 0

def ev_func(board):
    # The evaluation function J(x)
    return A * material(board) + B * cent_cont(board) + C * kingSafety(board) + D * mobiltity(board) + gameOver(board)


def sum_from(arr, t):  # This is our $\Delta t$
    n = len(arr)
    sum = 0
    lamb = 0.7
    for i in range(t, n):
        sum += (lamb ** (i - t)) * arr[i]
    return sum


def grad(board):
    # Gradient of J(x)
    return [material(board), cent_cont(board), kingSafety(board)]

def generateReward(board, move, count = 1): 
    # Assigns reward for each move based on depth
    brd = board.copy()
    if(count == depth):
        brd.push_san(str(move))
        if(brd.is_checkmate()):
            return ev_func(brd)
        temp = []
        print("Black loop 1")
        for BlackMove in brd.legal_moves:
            brd.push_san(str(BlackMove))
            temp.append(ev_func(brd))
            brd.pop()
        brd.pop()
        #print(temp)
        return min(temp)

    else:
        brd.push_san(str(move))
        if(brd.is_checkmate()):
            return ev_func(brd)
        black_eval = []
        for BlackMove in brd.legal_moves:
            brd.push_san(str(BlackMove))
            if(brd.is_checkmate()):
                black_eval.append(ev_func(brd))
                continue
            white_eval = []
            print("-------------------------------------")
            for WhiteMove in brd.legal_moves:
                print("WHITE LOOP 2")
                white_eval.append(generateReward(brd, WhiteMove, count + 1))
            if white_eval != []:
                black_eval.append(max(white_eval))
            brd.pop()
        brd.pop()
        #print(black_eval)
        return min(black_eval)

def simple_terminal_engine():
    # This function allows the user to play chess with the engine
    board = chess.Board()
    state_list = []
    brd = board.copy()
    state_list.append(brd)
    del(brd)
    print(state_list)
    if(man == False):
        engine = chess.engine.SimpleEngine.popen_uci(r"stockfish")
    while True:
        A = [[board ,i] for i in board.legal_moves]
        rewards = []

        # Making the engine think multiple moves simultaneously using multiprocessing
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
                    brd = board.copy()
                    state_list.append(brd)
                    del(brd)
                    print(state_list)
                    break
                except ValueError:
                    print("Invalid move. Please try again.")
        else:
            stock_move = engine.play(board, chess.engine.Limit(time=0.1))
            board.push(stock_move.move)
            brd = board.copy()
            state_list.append(brd)
            del(brd)
        print(board)
        dispBoard(board)
        if board.is_checkmate():
            state_list.append("L")
            break
        if board.is_insufficient_material():
            state_list.append("D")
            break
    if(man == False):
        engine.quit()
    return state_list


def engine_learn(a):
    # Making the engine learn from its mistakes 
    state_list = simple_terminal_engine()
    N = len(state_list) - 1  # Actual length of the game neglecting the final element
    rN = 0
    if state_list[N] == "W":
        rN = 100000*(A + B + C + D)
    elif state_list[N] == "L":
        rN = -100000*(A + B + C + D)
    d = []  # Temporal differences are stored here
    for t in range(0, N - 1):
        J_t = ev_func(state_list[t])
        J_tp = ev_func(state_list[t + 1])
        d.append(J_tp - J_t)
    J = ev_func(state_list[N - 1])
    d.append(rN - J)
    update = [A, B, C, D]  # This will contain the corrected coefficients
    for t in range(N):
        temp = grad(state_list[t])  # The gradient at a particular state
        delta_t = sum_from(d, t)  # This is our $\Delta t$
        for i in range(len(temp)):
            update[i] += temp[i] * delta_t * a
    return update


next_game = 1
while next_game == 1:
    if n == 0:
        print("Learnt")
        break
    l = engine_learn(n)
    # making sure that coefficients are never negative
    for i in range(len(l)):
        if(l[i] < 0):
            l[i] = 0
    # update of coefficients
    A = l[0]
    B = l[1]
    C = l[2]
    D = l[3]
    f = open("Parameters2.txt", "a") # Putting the updated coeff. in a file
    text = str(l) + "\n"
    f.write(text)
    f.close()
    print(l)
    next_game = int(input("Continue? (0 = No / 1 = Yes)"))
    n -= 1
    print(
        "--------------------------------------------------------------------------------------------------------"
    )

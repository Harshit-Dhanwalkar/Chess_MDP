import chess
import chess.engine
import chess.svg
import cv2
from cairosvg import svg2png

A = float(input("A = "))
B = float(input("B = "))
n = int(input("Number of games = "))
depth = int(input("depth = "))
man = bool(input("MANUAL = "))


def dispBoard(board):
    f = open("pic.svg", "w")
    a = chess.svg.board(board, flipped=man)
    f.write(a)
    f.close()
    svg2png(url="./pic.svg", write_to="./pic.png")
    image = cv2.imread("./pic.png")
    cv2.imshow("image window", image)
    # cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()


def material(board):
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
        whiteAttackers = len(board.attackers(chess.WHITE, square))
        blackAttackers = len(board.attackers(chess.BLACK, square))
        ret += (whiteAttackers - blackAttackers) * value[square]
    return ret


def ev_func(board):
    return A * material(board) + B * cent_cont(board)


def sum_from(arr, t):  # This is out $\Delta t$
    n = len(arr)
    sum = 0
    lamb = 0.7
    for i in range(t, n):
        sum += (lamb ** (i - t)) * arr[i]
    return sum


def grad(board):
    return [material(board), cent_cont(board)]


def generateMove(board, count=1):  # returns [move, evaluation]
    if count == depth:
        final_eval_arr = []
        A = [i for i in board.legal_moves]  # Creating action space
        print("Starting white block 1")
        for WhiteMove in A:
            board.push_san(str(WhiteMove))  # This function plays the move and modifies board
            temp = []
            print("Starting black block 1")
            for BlackMove in board.legal_moves:
                board.push_san(str(BlackMove))
                intermediate_eval = ev_func(board)
                temp.append(intermediate_eval)
                board.pop()  # Undo the last move
            final_eval_arr.append(min(temp))
            board.pop()
        final_eval = max(final_eval_arr)
        action_ind = final_eval_arr.index(final_eval)
        return [A[action_ind], final_eval]

    final_eval_arr = []
    A = [i for i in board.legal_moves]  
    print("Starting white block 2")
    for whiteMove in A:
        board.push_san(str(whiteMove))
        black_eval = []
        print("Starting black block 2")
        print("------------------------------------------------------------")
        for blackMove in board.legal_moves:
            board.push_san(str(blackMove))
            temp = generateMove(board, count + 1)
            black_eval.append(temp[1])
            board.pop()
        final_eval_arr.append(min(black_eval))
        board.pop()
    final_eval = max(final_eval_arr)
    action_ind = final_eval_arr.index(final_eval)
    return [A[action_ind], final_eval]


def simple_terminal_engine():
    # Create a chess board
    board = chess.Board()
    state_list = [board]
    engine = chess.engine.SimpleEngine.popen_uci(r"stockfish")
    while True:
        action = generateMove(board)
        board.push_san(str(action[0]))
        print("Engine move : ", action[0])
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


def engine_learn(a):
    state_list = simple_terminal_engine()
    N = len(state_list) - 1  # Actual length of the game neglecting the final element
    rN = 0
    if state_list[N] == "W":
        rN = 100 * (A + B)
    elif state_list[N] == "L":
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


while True:
    if n == 0:
        print("Learnt")
        break
    l = engine_learn(n)
    A = l[0]
    B = l[1]
    f = open("Parameters2.txt", "a")
    text = str(l) + "\n"
    f.write(text)
    f.close()
    print(l)
    n -= 1
    print(
        "--------------------------------------------------------------------------------------------------------"
    )

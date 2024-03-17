import chess
import chess.svg
import math
import base64
import cv2
from cairosvg import svg2png
from scipy.optimize import fsolve
from Chess import (
    encode_board,
    base64_to_int,
    simple_terminal_engine,
)

A = float(input("A = "))
B = float(input("B = "))
C = float(input("C = "))
D = float(input("D = "))


def func(x):
    return (
        A * math.sin(x) + B * math.cos(x) + C * math.atan(x) + D * (math.e ** (-(x**2)))
    )


def funcd(x):  # derivative of func(x)
    return (
        A * math.cos(x)
        - B * math.sin(x)
        + C * (1 / (1 + (x**2)))
        + D * ((math.e ** (-(x**2))) * (-2 * x))
    )


def compute_max():
    guess = []
    for i in range(0, 100, 10):
        try:
            temp = fsolve(funcd, i)
            guess.append(func(temp))
        except:
            break
    print(max(guess))


def sum_from(arr, t):  # This is out $\Delta t$
    n = len(arr)
    sum = 0
    lamb = 0.7
    for i in range(t, n):
        sum += (lamb ** (i - t)) * arr[i]
    return sum


def grad(x):
    return [math.sin(x), math.cos(x), math.atan(x), (math.e ** (-(x**2)))]


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
        temp = grad(x)  # The gradient at a particular state
        delta_t = sum_from(d, t)  # This is our $\Delta t$
        for i in range(len(temp)):
            update[i] += temp[i] * delta_t
    print(update)


<!-- BEGIN CHESS BOARD -->
|   | A | B | C | D | E | F | G | H |   |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **8** | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/black/bishop.png" width=50px> | <img src="img/black/knight.png" width=50px> | <img src="img/black/rook.png" width=50px> | **8** |
| **7** | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/black/pawn.png" width=50px> | <img src="img/black/king.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/black/pawn.png" width=50px> | **7** |
| **6** | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/black/pawn.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | **6** |
| **5** | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/black/pawn.png" width=50px> | <img src="img/black/pawn.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | **5** |
| **4** | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/black/rook.png" width=50px> | <img src="img/white/bishop.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | **4** |
| **3** | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/white/queen.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | **3** |
| **2** | <img src="img/white/pawn.png" width=50px> | <img src="img/white/pawn.png" width=50px> | <img src="img/white/pawn.png" width=50px> | <img src="img/white/king.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/white/pawn.png" width=50px> | <img src="img/white/pawn.png" width=50px> | <img src="img/white/pawn.png" width=50px> | **2** |
| **1** | <img src="img/white/rook.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/blank.png" width=50px> | <img src="img/white/rook.png" width=50px> | **1** |
|   | **A** | **B** | **C** | **D** | **E** | **F** | **G** | **H** |   |
<!-- END CHESS BOARD -->
---

# Chess_MDP
MDP & RL project

This is Markov's Decision Process and Reinforcement Learning Course Project
# Chess Automation using MDP, RL, Dynamic Programming, and ML

This repository contains the code for automating the game of Chess using Markov Decision Process (MDP), Reinforcement Learning (RL), Dynamic Programming, and Machine Learning (ML) techniques.

## Project Description

The goal of this project is to create a chess engine that can play at the level of a intermediate player in chess. This is done using the TD (\lambda) algorithm for the learning process and the minimax algorithm for playing.  

## Collaborators

- [Collaborator 1: Harshit Prahant Dhanwalkar](https://github.com/Harshit-Dhanwalkar)
- [Collaborator 2: Ganesh Arvindh](https://github.com/Phoenix-rd)

## Getting Started

To get started with this project, follow the instructions below:

1. Clone the repository: `git clone https://github.com/Harshit-Dhanwalkar/Chess-MDP.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the main script: `ChessEngine.py`

## Current Issues
- The minimax algorithm is very slow.This prevented us from finding the true strength of the engine. As of now, the best elo rating we have seen is 1000 at a depth of 2. The speed can be improved by using the alpha-beta pruning method. 




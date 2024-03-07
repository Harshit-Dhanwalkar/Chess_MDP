import chess
import chess.engine
import base64

def encode_board(board):
    # Encode the board using base64
    encoded_board = base64.b64encode(board.board_fen().encode('utf-8')).decode('utf-8')
    return encoded_board

def decode_board(encoded_board):
    # Decode the encoded board using base64
    decoded_board_fen = base64.b64decode(encoded_board.encode('utf-8')).decode('utf-8')
    board = chess.Board(decoded_board_fen)
    return board

def print_numbered_board(board):
    # Print the numbered chessboard
    print("   a b c d e f g h")
    print("  +----------------")
    for i in range(8, 0, -1):
        row = f"{i} |"
        for j in range(1, 9):
            square = chess.square(j - 1, i - 1)
            piece = board.piece_at(square)
            if piece is None:
                row += " ."
            else:
                row += " " + piece.symbol().replace(".", " ")
        print(row)

def simple_terminal_engine():
    # Create a chess board
    board = chess.Board()

    while not board.is_checkmate():
        # Print the numbered board
        print_numbered_board(board)

        # Encode and print the board
        encoded_board = encode_board(board)
        print("Encoded Board:", encoded_board)
        
        # Get the user's move
        move = input("Enter your move (e.g., 'e2e4'): ")
        
        # Validate and make the move
        if chess.Move.from_uci(move) in board.legal_moves:
            board.push_uci(move)
        else:
            print("Illegal move. Try again.")

        # Decode and print the board after the move
        decoded_board = decode_board(encoded_board)
        print("Decoded Board:")
        print_numbered_board(decoded_board)

    # Print the final board
    print_numbered_board(board)

simple_terminal_engine()

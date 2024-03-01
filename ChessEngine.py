# Updated by: Harshit

'''
This will responsible for storing inforamtion about the current state of chess game.
It will also be responsible for determining the valid moves at the current state.
It wil also keep a move log.
'''

class GameState():
    def __init__(self):
        # Board of 8x8 2D list, each element has 2 characters.
        # The first character represents the color of the piece (b/w)
        # The second character represents the type of the piece (K, Q, R, B, N, P)
        # "--" represents an empty space with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 
                              'N': self.getKnightMoves, 'B': self.getBishopMoves,
                              'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = () # coordinates for the square where en passant capture is possible
        #self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                            self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        
    '''
    Takes a Move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove # swap players
        # update the king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        
        # enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"
        # update enpassantPossible variable
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2: # only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()
        # update enpassantPossibleLog
        self.enpassantPossibleLog.append(self.enpassantPossible)        
        
        # castle move
        if move.isCastleMove:           
            if move.endCol - move.startCol == 2:     # King side castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] # Move the rook to the correct position
                self.board[move.endRow][move.endCol + 1] = '--'                                     # Clear the previous position of the rook
            else:                                   # Queen side castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2] # Move the rook to the correct position
                self.board[move.endRow][move.endCol - 2] = '--'                                     # Clear the previous position of the rook
        # update castling rights - whenever it is a rook or a king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                                self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
        
    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # switch turns back
            # update the king's location if moved
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            # undo enpassant move
            if move.isEnpassantMove: 
                self.board[move.endRow][move.endCol] = "--" #leave landing sq.
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            # undo a 2 square pawn advance
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()
            # undo castle right
            self.castleRightsLog.pop() # get rid of the new castle rights from the move we are undoing
            newRights = self.castleRightsLog[-1] # newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks,newRights.wks,newRights.bks,newRights.wqs,newRights.bqs)
            # undo castle move                                         self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs) # set the current castle rights to the last one in the list
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #king side
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1] # keep  the rook back
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:                                  #queen side
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1] # keep  the rook back
                    self.board[move.endRow][move.endCol + 1] = '--'
            self.checkMate = False
            self.staleMate = False

    '''
    Update the castle rights given the move
    '''
    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7: 
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRight.bks = False
        
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        ### for log in self.castleRightsLog:
        ###     print(log.wks,log.wqs,log.bks,log.bqs, end=", ")            
        ### print()
        
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)
        # generates all possible moves
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        #self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove: # white to move
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else: # black to move
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck: # if you are in check, you must move the king
            if len(self.checks) == 1: # only 1 check, block check or move king
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] # the piece giving the check
                validSquares = []
                if pieceChecking[1] == 'N': # if knight, must capture knight or move king, other pieces can block
                    validSquares = [(checkRow, checkCol)] # the only valid move is to capture the knight
                else: # king has to move or block the check
                    for i in range(1, 8): # king can move 1 square in any direction
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: # once you get to piece giving check, you can capture it
                            break
                for i in range(len(moves) - 1, -1, -1): # go through the list backwards when you are removing from a list
                    if moves[i].pieceMoved[1] != 'K': # king doesn't have to move
                        if not (moves[i].endRow, moves[i].endCol) in validSquares: # move doesn't block check or capture
                            moves.remove(moves[i])
            else: # double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: # not in check so all moves are fine
            moves = self.getAllPossibleMoves()
            if self.whiteToMove:
                self.getCastleMoves(kingRow, kingCol, moves)
        
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves
      
    '''
    Determine if the current player is in check
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
    
    '''
    Determine if the enemy can attack the square r, c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # switch to opponent's turn
        opponentMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove # switch turns back
        for move in opponentMoves:
            if move.endRow == r and move.endCol == c: # square is under attack
                return True
        return False
    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # number of rows
            for c in range(len(self.board[r])): # number of cols in given row
                turn = self.board[r][c][0] # get the color of the piece
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # call the appropriate move function
        return moves            
                        
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1): # go through the list backwards when you are removing from a list
            if self.pins[i][0] == r and self.pins[i][1] == c: # this is a pinned piece, so we can remove the pinning piece and see if we are still pinned
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
            
        if self.whiteToMove: # white pawn moves
            if self.board[r - 1][c] == "--": # 1 square pawn advance
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == "--": # 2 square pawn advance
                        moves.append(Move((r, c), (r-2, c), self.board))
            # caturing moves
            if c - 1 >= 0: # captures to the left
                if self.board[r - 1][c - 1][0] == 'b': # enemy piece to capture
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, enpassantPossible = True))
            if c + 1 < len(self.board): # captures to the right
                if self.board[r - 1][c + 1][0] == 'b': # enemy piece to capture
                    if not piecePinned or pinDirection == (-1, 1): # no piece blocking, so check
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, enpassantPossible = True))
            
        else: # black pawn moves
            if self.board[r + 1][c] == "--": # 1 square pawn advance
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--": # 2 square pawn advance
                        moves.append(Move((r, c), (r+2, c), self.board))
            # caturing moves
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w': # captures to the left
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, enpassantPossible = True))
            if c + 1 < len(self.board): # captures to the right
                if self.board[r + 1][c + 1][0] == 'w': # captures to the right
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, enpassantPossible = True))
     
    #add pawn promotion later

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1): # go through the list backwards when you are removing from a list
            if self.pins[i][0] == r and self.pins[i][1] == c: # this is a pinned piece, so we can remove the pinning piece and see if we are still pinned
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break
            
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, len(self.board)):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board): # on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: # enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: # friendly piece
                            break
                
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1): # go through the list backwards when you are removing from a list
            if self.pins[i][0] == r and self.pins[i][1] == c: # this is a pinned piece, so we can remove the pinning piece and see if we are still pinned
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
            
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # up-left, up-right, down-left, down-right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, len(self.board)):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board):
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):                                 
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: # friendly piece
                            break
                else: # off board
                    break

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1): # go through the list backwards when you are removing from a list
            if self.pins[i][0] == r and self.pins[i][1] == c: # this is a pinned piece, so we can remove the pinning piece and see if we are still pinned
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
            
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in directions:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board):
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
        self.getCastleMoves(r, c, moves)

    '''
    Generate all valid castle moves for the king at (r,c) and add them to the list of moves
    '''
    def getCastleMoves(self, r, c, moves):
        ###if self.inCheck():
        ###    return # we can't castle while in check
        
        ###if self.squareUnderAttack(r, c):
        ###    return  # cannot castle while in check

        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(r, c, moves)

    '''
    Generate all valid king side castle moves for the king at (r,c) and add them to the list of moves
    '''
    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--":
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    '''
    Generate all valid queen side castle moves for the king at (r,c) and add them to the list of moves
    '''
    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--":
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
        
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))
        self.getCastleMoves
    '''
    Return if the player is in check, a list of pins, and a list of checks
    '''
    def checkForPinsAndChecks(self):
        pins = [] # squares where allied pinned pieces are and direction pinned from
        checks = [] # squares where enemy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        # check outward from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)): # 8 directions
            d = directions[j]
            possiblePin = () # reset possible pins
            for i in range(1, len(self.board)): # check 1 to 7 squares away
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board):
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == (): # 1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: # 2nd allied piece, so no pin or check from this direction
                            break
                    elif endPiece[0] == enemyColor: 
                        type = endPiece[1]
                        # 5 possibilities here in this complex conditional
                        # 1. orthogonally away from king and piece is a rook
                        # 2. diagonally away from king and piece is a bishop
                        # 3. 1 square away diagonally from king and piece is a pawn
                        # 4. any direction and piece is a queen
                        # 5. any direction 1 square away and piece is a king
                        
                        if (0 <= j <= 3 and type == 'R') or (4 <= j <= 7 and type == 'B') or (i == 1 and type == 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == (): # no piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: # piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else: # enemy piece not applying check
                            break
                else: # off board
                    break
        # check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N': # enemy knight attacking the king
                    inCheck = True 
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks
       
    def changeTurn(self):
        self.whiteToMove = not self.whiteToMove

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs): # 
        self.wks = wks # white king side
        self.bks = bks # Black king side
        self.wqs = wqs # white queen side
        self.bqs = bqs # Black queen side

class Move():
    # Maps keys to values
    # key : value
    # (row, col) : (row, col)
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)
        # enpassant move
        self.isEnpassantMove = isEnpassantMove
        # castle move
        self.isCastleMove = isCastleMove
                           #(self.pieceMoved == 'wK' and self.startRow == 7) and (self.startCol == 4 and self.endRow == 7) and (self.endCol == 6 or self.pieceMoved == 'bK') and (self.startRow == 0 and self.startCol == 4) and (self.endRow == 0 and self.endCol == 6)

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #print(self.moveID)

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
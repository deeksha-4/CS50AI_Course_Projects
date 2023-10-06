"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    c=0
    for i in range(3):
        for j in range(3):
            if board[i][j]:
                c+=1
    
    if c%2==0:
        return 'X'
    return 'O'

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    s = set()
    for i in range(3):
        for j in range(3):
            if not board[i][j]:
                s.add(tuple((i, j)))
    return s
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    b = [row[:] for row in board]
    if not board[action[0]][action[1]]:
        b[action[0]][action[1]] = player(board)
        return b
    
    raise Exception("Invalid action")

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0]==board[0][1]==board[0][2]!=None:
        return board[0][0]
    if board[1][0]==board[1][1]==board[1][2]!=None:
        return board[1][0]
    if board[2][0]==board[2][1]==board[2][2]!=None:
        return board[2][0]
    if board[0][0]==board[1][0]==board[2][0]!=None:
        return board[0][0]
    if board[0][1]==board[1][1]==board[2][1]!=None:
        return board[0][1]
    if board[0][2]==board[1][2]==board[2][2]!=None:
        return board[0][2]
    if board[0][0]==board[1][1]==board[2][2]!=None:
        return board[0][0]
    if board[0][2]==board[1][1]==board[2][0]!=None:
        return board[2][0]
    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for i in range(3):
        for j in range(3):
            if not board[i][j]:
                return False
    return True

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
        return 1
    if winner(board) == 'O':
        return -1
    else:
        return 0

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    a = actions(board)
    d= {}
    for i in a:
        r = result(board, i)
        l = lookin(r)
        if l==1 and player(board)=="X":
            return i
        if l==-1 and player(board)=="O":
            return i
        d[l] = i
    return d[0]

    raise NotImplementedError

def lookin(board):
    p = player(board)
    s = set()

    if terminal(board):
        s.add(utility(board))

    else:
        ac = actions(board)
        for j in ac:
            res = result(board, j)
            s.add(lookin(res))   

    if p == "X":
        return max(s)
    else:
        return min(s)

    
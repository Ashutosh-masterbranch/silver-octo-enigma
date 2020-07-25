"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


# Helper functions
def get_diags(board):
    return [[board[0][0], board[1][1], board[2][2]],
            [board[0][2], board[1][1], board[2][0]]]

def all_cells_filled(board):
    for row in board:
        if EMPTY in row:
            return False

def three_in_a_row(row):
    return True if row.count(row[0]) == 3 else False

    return True
def get_columns(board):
    columns = []

    for i in range(3):
        columns.append([row[i] for row in board])

    return columns

def minimax_value(board, player, alpha, beta):
    if terminal(board):
        return utility(board)

    if player == X:
        v = -math.inf

        for action in actions(board):
            v = max(v, minimax_value(result(board, action), O, alpha, beta))

            alpha = max(alpha, v)

            if alpha >= beta:
                break

        return v
    else:
        v = math.inf

        for action in actions(board):
            v = min(v, minimax_value(result(board, action), X, alpha, beta))

            beta = min(beta, v)

            if alpha >= beta:
                break

        return v


# Tictactoe

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
    player_X = 0
    player_O = 0

    #following is the flatten_matrix to implement Counter on it
    for row in board:
        if X in row:
            player_X += row.count(X)

        if O in row:
            player_O += row.count(O)

    return X if player_X <= player_O else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    The actions function should return a set of all of the possible actions that can be taken on a given board.
    Each action should be represented as a tuple (i, j) where i corresponds to the row of the move (0, 1, or 2) and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).
    Possible moves are any cells on the board that do not already have an X or an O in them.
    Any return value is acceptable if a terminal board is provided as input.
    """
    possible_actions = set()

    for i, row in enumerate(board):
        if EMPTY in row:
            for j, space in enumerate(row):
                if space is EMPTY:
                    possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    The result function takes a board and an action as input, and should return a new board state, without modifying the original board.
    If action is not a valid action for the board, your program should raise an exception.
    The returned board state should be the board that would result from taking the original input board, and letting the player whose turn it is make their move at the cell indicated by the input action.
    Importantly, the original board should be left unmodified: since Minimax will ultimately require considering many different board states during its computation. This means that simply updating a cell in board itself is not a correct implementation of the result function. You’ll likely want to make a deep copy of the board first before making any changes.
    """
    i, j = action
    new_board = deepcopy(board)
    current_player = player(new_board)

    if new_board[i][j] is not EMPTY:
        raise Exception("Invalid action.")
    else:
        new_board[i][j] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    The winner function should accept a board as input, and return the winner of the board if there is one.
    If the X player has won the game, your function should return X. If the O player has won the game, your function should return O.
    One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
    assumming that there will be at most one winner (that is, no board will ever have both players with three-in-a-row, since that would be an invalid board state).
    If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the function should return None.
    """
    rows = board + get_diags(board) + get_columns(board)

    for row in rows:
        current_player = row[0]

        if current_player is not None and three_in_a_row(row):
            return current_player

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    The terminal function should accept a board as input, and return a boolean value indicating whether the game is over.
    If the game is over, either because someone has won the game or because all cells have been filled without anyone winning, the function should return True.
    Otherwise, the function should return False if the game is still in progress.
    """ 
    #checking for winning combination
    if winner(board) is not None:
        return True
    else:
        return all_cells_filled(board)


def utility(board):
     """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    The utility function should accept a terminal board as input and output the utility of the board.
    If X has won the game, the utility is 1. If O has won the game, the utility is -1. If the game has ended in a tie, the utility is 0.
    assumming that utility will only be called on a board if terminal(board) is True.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0          


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    The minimax function should take a board as input, and return the optimal move for the player to move on that board.
    The move returned should be the optimal action (i, j) that is one of the allowable actions on the board. If multiple moves are equally optimal, any of those moves is acceptable.
    If the board is a terminal board, the minimax function should return None.
    """
    if terminal(board):
        return None

    optimal_move = None

    alpha = -math.inf
    beta = math.inf

    if player(board) is X:
        v = -math.inf

        for action in actions(board):
            new_v = minimax_value(result(board, action),
                                  O, alpha, beta)

            alpha = max(v, new_v)

            if new_v > v:
                v = new_v
                optimal_move = action

    else:
        v = math.inf

        for action in actions(board):
            new_v = minimax_value(result(board, action),
                                  X, alpha, beta)

            beta = min(v, new_v)

            if new_v < v:
                v = new_v
                optimal_move = action

    return optimal_move
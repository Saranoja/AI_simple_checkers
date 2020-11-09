import copy
from math import inf

BOARD_SIZE = 4
EMPTY, HUMAN, COMPUTER = '⬛', '🔴', '🔷'

human_row = [HUMAN] * BOARD_SIZE
computer_row = [COMPUTER] * BOARD_SIZE
empty_rows = [[EMPTY] * BOARD_SIZE for i in range(BOARD_SIZE - 2)]
b = [computer_row, *empty_rows, human_row]


def print_board(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            print(board[i][j], end=" ")
        print()
    print()


def is_terminal_state(board):
    if board[0] == human_row or board[BOARD_SIZE - 1] == computer_row:
        return True
    return False


def get_neighbors(board, i, j):
    neighbor_positions = []
    for position in [(i + 1, j + 1), (i, j + 1), (i + 1, j), (i - 1, j - 1),
                     (i - 1, j + 1), (i - 1, j), (i, j - 1), (i + 1, j - 1)]:
        if 0 <= position[0] < BOARD_SIZE and 0 <= position[1] < BOARD_SIZE and board[position[0]][position[1]] == EMPTY:
            neighbor_positions.append(position)
    return neighbor_positions


def get_valid_moves(board, player):
    valid_moves = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == player:
                for neighbor in get_neighbors(board, i, j):
                    valid_moves.append([(i, j), neighbor])
    return valid_moves


# transition = [(i1, j1), (i2, j2)]
# move from (i1, j1) to (i2, j2)
def move_piece(board, transition):
    board[transition[1][0]][transition[1][1]] = board[transition[0][0]][transition[0][1]]
    board[transition[0][0]][transition[0][1]] = EMPTY


def get_board_states(board, player):
    board_states = []
    for move in get_valid_moves(board, player):
        board_copy = copy.deepcopy(board)
        move_piece(board_copy, move)
        board_states.append(board_copy)
    return board_states


def get_heuristic(board):
    """ Calculate heuristic given board state

    :param board:
     Board state to calculate heuristic for.
    :return:
     Number between [-8, 8], the higher the value the better move for the computer.
    """
    sum_advances_computer = sum_advances_human = 0
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == HUMAN:
                sum_advances_human += (BOARD_SIZE - 1) - i
            elif board[i][j] == COMPUTER:
                sum_advances_computer += (BOARD_SIZE - 1) - i
    return 12 - sum_advances_computer - sum_advances_human


def minimax(board, depth, is_max_player):
    """

    :param board:
    :param depth:
    :param is_max_player:
    :return:
    """
    if is_max_player:  # the computer is currently taking the turn
        # calculate the maximum value along descendants of the current node
        max_value, max_board = calculate_max(board, depth)
        board = max_board
    elif not is_max_player:  # the human is currently taking the turn
        # calculate the minimum value along descendants of the current node
        min_value, min_board = calculate_min(board, depth)
        board = min_board
    return board


def calculate_max(board, depth):
    """

    :param board:
    :param depth:
    :return: Returns maximum heuristic value from direct descendants
    """
    if depth == 0 or is_terminal_state(board):
        return get_heuristic(board), [[]]

    max_board = None
    max_value = -inf
    for board_state in get_board_states(board, COMPUTER):
        board_state_value, _ = calculate_min(board_state, depth - 1)
        if board_state_value > max_value:
            max_value = board_state_value
            max_board = board_state

    print('Heuristic value for max board:', max_value)
    print_board(max_board)
    return max_value, max_board


def calculate_min(board, depth):
    """

    :param board:
    :param depth:
    :return: Returns minimum heuristic value from direct descendants
    """
    if depth == 0 or is_terminal_state(board):
        return get_heuristic(board), [[]]

    min_board = None
    min_value = +inf
    for board_state in get_board_states(board, HUMAN):
        board_state_value, _ = calculate_max(board_state, depth - 1)
        if min_value > board_state_value:
            min_value = board_state_value
            min_board = board_state

    print('Heuristic value for min board', min_value)
    print_board(min_board)
    return min_value, min_board


example_board = [
    [EMPTY, EMPTY, EMPTY, EMPTY, ],
    [EMPTY, COMPUTER, HUMAN, EMPTY, ],
    [HUMAN, HUMAN, EMPTY, HUMAN, ],
    [COMPUTER, COMPUTER, COMPUTER, EMPTY, ],
]

print_board(minimax(example_board, 3, False))  # changes decision for depth=4
# print_board(minimax(example_board, 3, True))

import copy

BOARD_SIZE = 4
EMPTY, HUMAN, COMPUTER = '◻', '🔴', '🔷'

# initial configuration
empty_rows = [[EMPTY] * BOARD_SIZE for i in range(BOARD_SIZE - 2)]
human_row = [[HUMAN] * BOARD_SIZE]
computer_row = [[COMPUTER] * BOARD_SIZE]
# board will always keep the current state of the game
board = [*computer_row, *empty_rows, *human_row]


def pretty_print_board(b):
    for i in range(BOARD_SIZE):
        for j in b[i]:
            print(j, end=' ')
        print()


# final state check
def is_game_over():
    if board[0] == human_row[0] or board[BOARD_SIZE - 1] == computer_row[0]:
        return True
    else:
        return False


# F = 12 - sum(yc) - sum(yh) where y are coordinates for each of the players' positions
def heuristic(possible_board_configuration):
    syc = 0
    syh = 0
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if possible_board_configuration[i][j] == HUMAN:
                syh += 3 - i
            elif possible_board_configuration[i][j] == COMPUTER:
                syc += i
    return 12 - syc - syh


# given a position (i,j), return all the neighbours that are available
def get_neighbors(a, b):
    return [element for element in
            [(a + 1, b + 1), (a, b + 1), (a + 1, b), (a - 1, b + 1), (a - 1, b), (a, b - 1), (a + 1, b - 1)]
            if 0 <= element[0] < BOARD_SIZE and 0 <= element[1] < BOARD_SIZE and board[element[0]][
                element[1]] == EMPTY]


def get_valid_moves():
    valid_moves = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == COMPUTER:
                for neighbour in get_neighbors(i, j):
                    valid_moves.append([(i, j), neighbour])
    return valid_moves


# move form: [(a,b),(c,d)]
def move_piece(transition, safe_board):
    safe_board[transition[1][0]][transition[1][1]] = safe_board[transition[0][0]][transition[0][1]]
    safe_board[transition[0][0]][transition[0][1]] = EMPTY


def get_best_move(valid_moves):
    best_score_yet = -100
    best_move_yet = []
    for move in valid_moves:
        board_copy = copy.deepcopy(board)
        move_piece(move, board_copy)
        if heuristic(board_copy) > best_score_yet:
            best_score_yet = heuristic(board_copy)
            best_move_yet = move
    return best_move_yet


# move form: [(a,b),(c,d)]
def is_valid_move_from_user(move):
    if board[move[0][0]][move[0][1]] == HUMAN and board[move[1][0]][move[1][1]] == EMPTY and move[1] in get_neighbors(
            move[0][0], move[0][1]):
        return True
    else:
        return False


def play_game():
    print("Game on")
    pretty_print_board(board)
    while not is_game_over():
        move_from = (0, 0)
        move_to = (0, 0)
        print("Your turn: ")
        while not is_valid_move_from_user([move_from, move_to]):
            user_piece_to_move = input('Enter coordinates of the piece you want to move, separated by space: ')
            where_to_move = input('Enter coordinates of the cell you want to place the piece on, separated by space: ')
            move_from = tuple(map(int, user_piece_to_move.split()))
            move_to = tuple(map(int, where_to_move.split()))
            if not is_valid_move_from_user([move_from, move_to]):
                print("Try again :)")
        move_piece([move_from, move_to], board)
        print(f'Computer moved from {get_best_move(get_valid_moves())[0]} to {get_best_move(get_valid_moves())[1]}')
        move_piece(get_best_move(get_valid_moves()), board)
        pretty_print_board(board)


play_game()

# example_board = [*human_row, *computer_row, *empty_rows]
# pretty_print_board(example_board)
# print(heuristic(example_board))

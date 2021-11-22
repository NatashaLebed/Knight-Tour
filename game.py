def get_dimensions():
    global cols, rows
    while True:
        try:
            cols, rows = [int(num) for num in input('Enter your board dimensions:').split()]
            assert cols > 0 and rows > 0
        except (TypeError, ValueError, AssertionError):
            print("Invalid dimensions!")
        else:
            return cols, rows


def get_cell_size():
    return len(str(cols * rows))


def create_board():
    return [[empty_cell] * cols for _ in range(rows)]


def get_position(input_text):
    while True:
        try:
            x, y = [int(num) for num in input(input_text).split()]
            assert 1 <= x <= cols and 1 <= y <= rows
        except (TypeError, ValueError, AssertionError):
            print("Invalid position!")
        else:
            return user_pos_to_real_pos(x, y)


def user_pos_to_real_pos(x, y):
    return rows - y, x - 1


def get_possible_moves(x, y):
    steps = [[2, 1], [2, -1], [1, 2], [-1, 2], [1, -2], [-1, -2], [-2, -1], [-2, 1]]
    moves = []

    for i in range(8):
        next_x = x + steps[i][0]
        next_y = y + steps[i][1]
        if 0 <= next_x <= (rows - 1) and 0 <= next_y <= (cols - 1) \
                and board[next_x][next_y] == empty_cell:
            moves.append([next_x, next_y])
    return moves


def mark_cell(x, y, char):
    board[x][y] = char.rjust(cell_size)


def mark_possible_moves(_moves):
    for [x, y] in _moves:
        num_moves = len(get_possible_moves(x, y))
        mark_cell(x, y, str(num_moves))


def next_move(moves):
    while True:
        x, y = get_position("Enter your next move:")
        if [x, y] in moves:
            return x, y
        else:
            print('Invalid move! ', end='')


def del_prev_possible_moves(moves):
    for [x, y] in moves:
        board[x][y] = empty_cell


def play_game(x, y):
    visited = 1
    while True:
        mark_cell(x, y, 'X')
        moves = get_possible_moves(x, y)
        mark_possible_moves(moves)
        print_matrix(board)

        if visited == cols * rows:
            print("What a great tour! Congratulations!")
            break
        elif not moves:
            print("No more possible moves!")
            print(f"Your knight visited {visited} squares!")
            break
        else:
            (prev_x, prev_y) = (x, y)
            x, y = next_move(moves)
            visited += 1
            mark_cell(prev_x, prev_y, '*')
            del_prev_possible_moves(moves)


def solution(x, y, counter):

    board[x][y] = str(counter).rjust(cell_size)
    if counter == cols * rows:
        return True
    moves = get_possible_moves(x, y)
    for [next_x, next_y] in moves:
        if solution(next_x, next_y, counter + 1):
            return True
        else:
            board[next_x][next_y] = empty_cell
    return False


def print_matrix(matrix):
    sep_line = '-' * (cols * 3 + 3)  # '---------------' length depends on number_of_columns
    print(f' {sep_line}')
    for i in range(rows):
        print(rows - i, end='')
        print('|', *matrix[i], '|')
    print(f' {sep_line}')
    bottom_line = [i for i in range(1, cols + 1)]  # '   1 2 3 ...... number_of_columns'
    print('  ', *bottom_line, sep=' ' * cell_size)
    print()


cols, rows = get_dimensions()
cell_size = get_cell_size()
empty_cell = '_' * cell_size  # depend on columns number default cell = '_' or '__' or '___'
board = create_board()
start_x, start_y = get_position("Enter the knight's starting position:")

while True:
    ans = input('Do you want to try the puzzle? (y/n):')
    if ans in ('y', 'n') and not solution(start_x, start_y, 1):
        print('No solution exists!')
        break
    elif ans == 'y':
        board = create_board()
        play_game(start_x, start_y)
        break
    elif ans == 'n':
        print("\nHere's the solution!")
        print_matrix(board)
        break
    else:
        print('Invalid input!')

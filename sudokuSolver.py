from itertools import product


def get_empty_cell(board):
    for row, column in product(range(9), repeat=2):
        if board[row][column] == 0:
            return row, column

    return None, None


def check_row(board, row, value):
    return value not in board[row]


def check_column(board, column, value):
    for row in range(9):
        if board[row][column] == value:
            return False

    return True


def check_box(board, row, column, value):
    row_start = (row // 3) * 3
    column_start = (column // 3) * 3

    for row, column in product(range(row_start, row_start + 3), range(column_start, column_start + 3)):
        if board[row][column] == value:
            return False

    return True


def is_valid(board, row, column, value):
    is_row_valid = check_row(board, row, value)
    is_column_valid = check_column(board, column, value)
    is_box_valid = check_box(board, row, column, value)

    if is_row_valid and is_column_valid and is_box_valid:
        return True

    return False


def solve_sudoku(board):
    row, column = get_empty_cell(board)

    if row is None:
        return True

    for value in range(1, 10):
        if is_valid(board, row, column, value):
            board[row][column] = value
            if solve_sudoku(board):
                return True

        board[row][column] = 0

    return False

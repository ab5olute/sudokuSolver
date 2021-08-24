from itertools import product
from typing import Optional


def get_empty_cell(board: list[list[int]]) -> tuple[Optional[int], Optional[int]]:
    for row, column in product(range(9), repeat=2):
        if board[row][column] == 0:
            return row, column

    return None, None


def check_row(board: list[list[int]], row: int, value: int) -> bool:
    return value not in board[row]


def check_column(board: list[list[int]], column: int, value: int) -> bool:
    for row in range(9):
        if board[row][column] == value:
            return False

    return True


def check_box(board: list[list[int]], row: int, column: int, value: int) -> bool:
    row_start: int = (row // 3) * 3
    column_start: int = (column // 3) * 3

    for row, column in product(range(row_start, row_start + 3), range(column_start, column_start + 3)):
        if board[row][column] == value:
            return False

    return True


def is_valid(board: list[list[int]], row: int, column: int, value: int) -> bool:
    is_row_valid = check_row(board, row, value)
    is_column_valid = check_column(board, column, value)
    is_box_valid = check_box(board, row, column, value)

    return is_row_valid and is_column_valid and is_box_valid


def solve_sudoku(board: list[list[int]]) -> bool:
    row: Optional[int]
    column: Optional[int]
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

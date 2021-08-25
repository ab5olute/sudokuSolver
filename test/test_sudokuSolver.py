import os
from copy import deepcopy
from unittest import TestCase, main

from sudokuSolver import get_empty_cell, solve_sudoku, check_row, check_column, check_box, read_sudoku


class TestSudokuSolver(TestCase):
    def setUp(self) -> None:
        self.board_easy: list[list[int]] = [
            [7, 0, 8, 5, 0, 6, 9, 2, 1],
            [3, 0, 9, 0, 0, 0, 4, 0, 0],
            [6, 0, 1, 8, 9, 4, 0, 3, 5],
            [0, 0, 5, 0, 0, 0, 2, 0, 0],
            [0, 6, 0, 9, 7, 0, 0, 1, 0],
            [0, 1, 4, 3, 0, 5, 0, 0, 0],
            [0, 9, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 6, 0, 0, 0, 0, 5, 7],
            [0, 0, 0, 4, 5, 0, 6, 0, 2],
        ]
        self.board_easy_answer: list[list[int]] = [
            [7, 4, 8, 5, 3, 6, 9, 2, 1],
            [3, 5, 9, 7, 2, 1, 4, 8, 6],
            [6, 2, 1, 8, 9, 4, 7, 3, 5],
            [9, 7, 5, 1, 4, 8, 2, 6, 3],
            [8, 6, 3, 9, 7, 2, 5, 1, 4],
            [2, 1, 4, 3, 6, 5, 8, 7, 9],
            [5, 9, 2, 6, 1, 7, 3, 4, 8],
            [4, 3, 6, 2, 8, 9, 1, 5, 7],
            [1, 8, 7, 4, 5, 3, 6, 9, 2]
        ]

        self.board_medium: list[list[int]] = [
            [0, 2, 0, 0, 0, 0, 0, 0, 3],
            [6, 0, 0, 0, 3, 0, 0, 5, 7],
            [0, 0, 0, 2, 7, 0, 0, 8, 4],
            [4, 0, 6, 7, 0, 0, 0, 0, 2],
            [0, 1, 0, 0, 9, 0, 0, 0, 0],
            [7, 0, 0, 0, 8, 0, 1, 0, 6],
            [1, 8, 0, 0, 0, 0, 0, 2, 9],
            [9, 0, 0, 0, 1, 4, 3, 0, 0],
            [0, 7, 0, 0, 0, 0, 5, 0, 0]
        ]
        self.board_medium_answer = [
            [8, 2, 7, 9, 4, 5, 6, 1, 3],
            [6, 4, 9, 1, 3, 8, 2, 5, 7],
            [5, 3, 1, 2, 7, 6, 9, 8, 4],
            [4, 9, 6, 7, 5, 1, 8, 3, 2],
            [2, 1, 8, 6, 9, 3, 7, 4, 5],
            [7, 5, 3, 4, 8, 2, 1, 9, 6],
            [1, 8, 5, 3, 6, 7, 4, 2, 9],
            [9, 6, 2, 5, 1, 4, 3, 7, 8],
            [3, 7, 4, 8, 2, 9, 5, 6, 1]
        ]

        self.board_hard = [
            [0, 0, 0, 2, 7, 6, 9, 8, 0],
            [9, 0, 0, 1, 0, 0, 0, 0, 7],
            [0, 0, 0, 0, 0, 0, 6, 0, 3],
            [0, 0, 4, 0, 0, 1, 0, 0, 2],
            [0, 1, 0, 0, 0, 0, 7, 0, 0],
            [3, 0, 0, 4, 8, 2, 0, 0, 0],
            [0, 0, 1, 0, 0, 7, 0, 0, 0],
            [2, 0, 0, 5, 0, 0, 0, 7, 8],
            [4, 0, 3, 0, 2, 0, 0, 0, 0]
        ]
        self.board_hard_answer = [
            [1, 3, 5, 2, 7, 6, 9, 8, 4],
            [9, 4, 6, 1, 3, 8, 2, 5, 7],
            [7, 2, 8, 9, 4, 5, 6, 1, 3],
            [6, 9, 4, 7, 5, 1, 8, 3, 2],
            [8, 1, 2, 6, 9, 3, 7, 4, 5],
            [3, 5, 7, 4, 8, 2, 1, 9, 6],
            [5, 8, 1, 3, 6, 7, 4, 2, 9],
            [2, 6, 9, 5, 1, 4, 3, 7, 8],
            [4, 7, 3, 8, 2, 9, 5, 6, 1]
        ]

        self.board_expert = [
            [0, 0, 0, 0, 2, 3, 4, 7, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 0, 9, 0, 4, 0, 5, 0, 0],
            [0, 7, 3, 0, 0, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 6, 0, 1, 0, 0, 4, 0],
            [1, 0, 0, 0, 0, 8, 0, 0, 4],
            [5, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 9, 0, 0, 6, 8, 0]
        ]
        self.board_expert_answer = [
            [6, 8, 5, 1, 2, 3, 4, 7, 9],
            [7, 3, 4, 5, 8, 9, 1, 6, 2],
            [2, 1, 9, 7, 4, 6, 5, 3, 8],
            [4, 7, 3, 2, 6, 5, 8, 9, 1],
            [8, 5, 1, 3, 9, 4, 7, 2, 6],
            [9, 2, 6, 8, 1, 7, 3, 4, 5],
            [1, 9, 7, 6, 3, 8, 2, 5, 4],
            [5, 6, 8, 4, 7, 2, 9, 1, 3],
            [3, 4, 2, 9, 5, 1, 6, 8, 7]
        ]

    def test_get_empty_cell(self):
        empty_cell: tuple[int, int] = (0, 1)
        self.assertEqual(empty_cell, get_empty_cell(self.board_easy))

    def test_check_row(self):
        self.assertFalse(check_row(self.board_easy, 0, 7))
        self.assertTrue(check_row(self.board_easy, 0, 4))

    def test_check_column(self):
        self.assertFalse(check_column(self.board_easy, 0, 7))
        self.assertTrue(check_column(self.board_easy, 0, 9))

    def test_check_box(self):
        self.assertFalse(check_box(self.board_easy, 1, 1, 7))
        self.assertTrue(check_box(self.board_easy, 1, 1, 5))

    def test_is_valid(self):
        self.assertFalse(check_box(self.board_easy, 1, 1, 7))
        self.assertTrue(check_box(self.board_easy, 1, 1, 5))

    def test_solve_easy(self):
        board: list[list[int]] = deepcopy(self.board_easy)
        solve_sudoku(board)
        self.assertEqual(self.board_easy_answer, board)

    def test_solve_medium(self):
        board: list[list[int]] = deepcopy(self.board_medium)
        solve_sudoku(board)
        self.assertEqual(self.board_medium_answer, board)

    def test_solve_hard(self):
        board: list[list[int]] = deepcopy(self.board_hard)
        solve_sudoku(board)
        self.assertEqual(self.board_hard_answer, board)

    def test_solve_expert(self):
        board: list[list[int]] = deepcopy(self.board_expert)
        solve_sudoku(board)
        self.assertEqual(self.board_expert_answer, board)

    def test_read_sudoku(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path: str = 'board_example.txt'
        conf_path: str = os.path.join(dir_path, path)

        expected_board: list[list[int]] = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                                           [6, 0, 0, 1, 9, 5, 0, 0, 0],
                                           [0, 9, 8, 0, 0, 0, 0, 6, 0],
                                           [8, 0, 0, 0, 6, 0, 0, 0, 3],
                                           [4, 0, 0, 8, 0, 3, 0, 0, 1],
                                           [7, 0, 0, 0, 2, 0, 0, 0, 6],
                                           [0, 6, 0, 0, 0, 0, 2, 8, 0],
                                           [0, 0, 0, 4, 1, 9, 0, 0, 5],
                                           [0, 0, 0, 0, 8, 0, 0, 7, 9]]
        self.assertEqual(read_sudoku(conf_path), expected_board)


if __name__ == '__main__':
    main()

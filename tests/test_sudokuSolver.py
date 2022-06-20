import unittest
import numpy as np

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.sudoku_solver import SudokuSolver

class TestSudokuSolver(unittest.TestCase):

    def test_isValid(self):
        board = np.array([
            [6, 0, 0, 0, 0, 0, 3, 7, 9],
            [7, 3, 2, 6, 9, 1, 0, 0, 8],
            [8, 4, 9, 3, 5, 0, 1, 0, 0],
            [0, 0, 3, 2, 0, 0, 4, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 7, 0, 8, 9, 0, 0, 0],
            [0, 0, 8, 1, 2, 0, 0, 0, 0],
            [5, 0, 6, 0, 3, 0, 7, 0, 4],
            [2, 0, 0, 5, 0, 0, 8, 1, 3]
            ], np.int32)
        solver = SudokuSolver()
        self.assertFalse(solver.isValid(board, 0, 1, 3))
        self.assertTrue(solver.isValid(board, 0, 1, 5))

    def test_backtracking_algo(self):
        board = np.array([
            [0, 0, 0, 0, 0, 0, 3, 7, 9],
            [7, 3, 2, 6, 9, 1, 0, 0, 8],
            [8, 4, 9, 3, 5, 0, 1, 0, 0],
            [0, 0, 3, 2, 0, 0, 4, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 7, 0, 8, 9, 0, 0, 0],
            [0, 0, 8, 1, 2, 0, 0, 0, 0],
            [5, 0, 6, 0, 3, 0, 7, 0, 4],
            [2, 0, 0, 5, 0, 0, 8, 1, 3]
            ], np.int32)
        expected_board = np.array([
            [6, 5, 1, 8, 4, 2, 3, 7, 9],
            [7, 3, 2, 6, 9, 1, 5, 4, 8],
            [8, 4, 9, 3, 5, 7, 1, 6, 2],
            [9, 6, 3, 2, 1, 5, 4, 8, 7],
            [4, 8, 5, 7, 6, 3, 2, 9, 1],
            [1, 2, 7, 4, 8, 9, 6, 3, 5],
            [3, 7, 8, 1, 2, 4, 9, 5, 6],
            [5, 1, 6, 9, 3, 8, 7, 2, 4],
            [2, 9, 4, 5, 7, 6, 8, 1, 3]
            ], np.int32)
        solver = SudokuSolver()
        solver.solveSudoku(board)
        np.testing.assert_array_equal(board, expected_board, err_msg='', verbose=True)

if __name__ == '__main__':
    unittest.main()
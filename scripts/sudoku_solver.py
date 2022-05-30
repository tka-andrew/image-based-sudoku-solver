import numpy

class SudokuSolver:
    def solveSudoku(self, board: numpy.ndarray) -> None:
        self.backtrack(board, 0, 0)
        
    def backtrack(self, board: numpy.ndarray, i: int, j: int) -> None:
        if (j==9):
            return self.backtrack(board, i+1, 0)
        if (i==9):
            return True
        if (board[i,j] != 0):
            return self.backtrack(board, i, j+1)
        num_list = [*range(1, 10, 1)]
        for num in num_list:
            if (not self.isValid(board, i, j, num)):
                continue
            board[i,j]=num
            if (self.backtrack(board, i, j+1)):
                return True # return true to stop backtrack
            board[i,j]=0
        return False
    
    def isValid(self, board: numpy.ndarray, r: int, c: int, num: int) -> bool:
        for i in range(0,9):
            if board[r,i] == num:
                return False
            if board[i,c] == num:
                return False          
            board_x = (r//3)*3 + i//3
            board_y = (c//3)*3 + i%3
            if (board[board_x, board_y] == num):
                return False
        return True
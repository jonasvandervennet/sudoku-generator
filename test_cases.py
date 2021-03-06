import unittest
from sudoku.sudoku import Sudoku


class TestSpecificExamples(unittest.TestCase):

    def test_easy(self):
        custom_input = [
            [0,0,0,8,0,4,0,5,0],
            [8,0,7,0,5,6,4,0,1],
            [0,6,0,1,0,0,2,0,0],
            [0,0,0,7,6,3,0,0,0],
            [0,7,0,0,0,0,0,4,0],
            [0,0,0,2,4,1,0,0,0],
            [0,0,6,0,0,5,0,2,0],
            [9,0,5,4,7,0,6,0,8],
            [0,8,0,6,0,9,0,0,0],
        ]
        expected_result = [
            [1, 9, 3, 8, 2, 4, 7, 5, 6],
            [8, 2, 7, 9, 5, 6, 4, 3, 1],
            [5, 6, 4, 1, 3, 7, 2, 8, 9],
            [2, 4, 8, 7, 6, 3, 1, 9, 5],
            [6, 7, 1, 5, 9, 8, 3, 4, 2],
            [3, 5, 9, 2, 4, 1, 8, 6, 7],
            [7, 1, 6, 3, 8, 5, 9, 2, 4],
            [9, 3, 5, 4, 7, 2, 6, 1, 8],
            [4, 8, 2, 6, 1, 9, 5, 7, 3],
        ]
        sudoku_example = Sudoku(size=9, custom=custom_input)
        sudoku_result = Sudoku(size=9, custom=expected_result)
        self.assertTrue(sudoku_example.solve_smart().equals(sudoku_result))
        
    def test_expert(self):
        custom_input = [
            [0,0,1,3,0,6,4,0,0],
            [0,0,0,1,0,0,0,0,3],
            [0,6,0,0,5,0,0,0,9],
            [9,0,6,0,0,2,0,7,0],
            [0,4,0,0,7,0,0,0,6],
            [2,0,0,0,0,0,0,0,4],
            [0,0,7,0,0,0,0,1,0],
            [0,5,0,0,9,0,0,0,0],
            [0,0,0,0,0,8,6,0,0],
        ]
        expected_result = [
            [7, 9, 1, 3, 2, 6, 4, 8, 5],
            [5, 2, 4, 1, 8, 9, 7, 6, 3],
            [8, 6, 3, 4, 5, 7, 1, 2, 9],
            [9, 3, 6, 8, 4, 2, 5, 7, 1],
            [1, 4, 8, 9, 7, 5, 2, 3, 6],
            [2, 7, 5, 6, 1, 3, 8, 9, 4],
            [3, 8, 7, 5, 6, 4, 9, 1, 2],
            [6, 5, 2, 7, 9, 1, 3, 4, 8],
            [4, 1, 9, 2, 3, 8, 6, 5, 7],
        ]
        sudoku_example = Sudoku(size=9, custom=custom_input)
        sudoku_result = Sudoku(size=9, custom=expected_result)
        self.assertTrue(sudoku_example.solve_smart().equals(sudoku_result))


if __name__ == '__main__':
    unittest.main()

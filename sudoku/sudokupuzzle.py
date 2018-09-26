from sudoku import Sudoku

"""
Create a solvable puzzle.
The solution to the puzzle should be unique.

Keep track of a score indicating difficulty:
B = branch-difficulty score by summing (Bi - 1)^2 at each node, where Bi are the branch factors
final score S = B * 100 + E, whrere E are the empty nodes.
(https://dlbeer.co.nz/articles/sudoku.html)
"""


class SudokuPuzzle(Sudoku):
    def __init__(self, **kwargs):
        diff = kwargs.pop('difficulty', None)
        self.difficulty = diff
        super().__init__(**kwargs)

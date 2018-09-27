from sudoku.sudoku import Sudoku

"""
Create a solvable puzzle.
The solution to the puzzle should be unique.

Keep track of a score indicating difficulty:
B = branch-difficulty score by summing (Bi - 1)^2 at each node, where Bi are the branch factors
final score S = B * 100 + E, whrere E are the empty nodes.
(https://dlbeer.co.nz/articles/sudoku.html)
"""


class SudokuPuzzle():
    def __init__(self, size=9, custom=None, verbose=False):
        """
        Accepts the following kwargs: size, custom and verbose.
        Uses these kwargs to initialise a 'solution' Sudoku, unless custom input was provided.
        In that case, an original sudoku is initialised and then solved to create the solution.
        """
        self.size = size
        if custom is not None:
            self.original = Sudoku(size=size, custom=custom, verbose=verbose)
            self.solution, branching = self.original.solve_smart(returnBranching=True)
        else:
            self.original = Sudoku(size=size, verbose=verbose)  # Fully blank canvas, to be filled later on from the solution

        self.solution, branching = self.original.solve_smart(returnBranching=True)
        self.difficulty = branching * 100 + self.original.empty
        self.calculation_time = self.solution.calculation_time  # Calc_time in ms!

    def generatePuzzleFromSolution(self):
        print(self.solution)

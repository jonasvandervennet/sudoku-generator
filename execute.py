from sudoku.sudoku import Sudoku
from sudoku.sudokupuzzle import SudokuPuzzle

custom_easy = [
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

custom_expert = [
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

custom_16 = [
    [3, 10, 12, 11, 5, 1, 6, 7, 2, 15, 8, 16, 13, 14, 9, 4],
    [1, 8, 15, 16, 13, 14, 12, 9, 4, 6, 7, 11, 3, 5, 2, 10],
    [13, 9, 6, 2, 4, 16, 15, 8, 3, 14, 5, 10, 1, 7, 11, 12],
    [5, 4, 14, 7, 10, 2, 3, 11, 9, 1, 12, 13, 8, 6, 16, 15],
    [10, 7, 11, 9, 2, 12, 14, 15, 16, 5, 3, 8, 6, 4, 1, 13],
    [8, 2, 1, 3, 11, 9, 5, 4, 14, 12, 13, 6, 15, 10, 7, 16],
    [6, 14, 4, 5, 1, 8, 13, 16, 11, 10, 15, 7, 12, 9, 3, 2],
    [12, 15, 16, 13, 3, 6, 7, 10, 1, 4, 9, 2, 14, 8, 5, 11],
    [9, 12, 7, 10, 16, 11, 4, 14, 13, 8, 2, 3, 5, 15, 6, 1],
    [11, 5, 2, 1, 6, 7, 9, 12, 15, 16, 4, 14, 10, 13, 8, 3],
    [15, 16, 13, 14, 8, 3, 10, 2, 5, 9, 6, 1, 11, 12, 4, 7],
    [4, 3, 8, 6, 15, 5, 1, 13, 7, 11, 10, 12, 2, 16, 14, 9],
    [16, 6, 3, 8, 12, 15, 11, 1, 10, 7, 14, 4, 9, 2, 13, 5],
    [2, 11, 10, 4, 9, 13, 8, 6, 12, 3, 16, 5, 7, 1, 15, 14],
    [7, 13, 5, 15, 14, 10, 16, 3, 6, 2, 1, 9, 4, 11, 12, 8],
    [14, 1, 9, 12, 7, 4, 2, 5, 8, 13, 11, 15, 16, 3, 10, 6],
]


def makelist(iterable, verbose=False):
    sudokulist = []
    for i in iterable:
        sudokulist.append(Sudoku(size=i * i, verbose=verbose))

    for sudoku in sudokulist:
        print(f'{sudoku.size}x{sudoku.size}: {sudoku.calculation_time}s')


# sc = Sudoku(size=9, custom=custom_easy, verbose=True)
# sc.solve()
# sc2 = Sudoku(size=9, custom=custom_expert, verbose=True)
# s16 = Sudoku(size=16, verbose=True)
# s16c = Sudoku(size=16, custom=custom_16, verbose=True)
# s25 = Sudoku(size=25, verbose=True)
# makelist([5] * 15, verbose=True)

def score(s):
    """
    Score a sudoku
    """
    empty = 0
    for node in s.nodes:
        if node.value == 0:
            empty += 1
    print(f'{empty} empty values')
    return empty
    #  TODO: branch factors


def generate():
    sudoku = Sudoku(size=9, solve=True)  # randomized pre-filled board
    print(sudoku.branchingFactor * 100 + score(sudoku))


custom_score_551 = [
    [3,7,0,0,0,9,0,0,6],
    [8,0,0,1,0,3,0,7,0],
    [0,0,0,0,0,0,0,0,8],
    [0,2,0,0,8,0,0,0,5],
    [1,8,7,0,0,0,6,4,2],
    [5,0,0,0,2,0,0,1,0],
    [7,0,0,0,0,0,0,0,0],
    [0,5,0,6,0,2,0,0,7],
    [2,0,0,3,0,0,0,6,1],
]
custom_score_253 = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
]

sp = SudokuPuzzle(size=9, verbose=False, custom=custom_score_551)
print(sp.difficulty)
print(sp.original.empty)

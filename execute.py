import time

from sudoku.sudoku import Sudoku
from sudoku.sudokupuzzle import SudokuPuzzle
from sudoku.textfiles import board2text


for i in range(1,6):
    print(i)
    total_start = time.time()
    sp = SudokuPuzzle(size=9, verbose=False, _diff=1000, _retries=100)
    total_time = time.time() - total_start
    print(f'Size: {sp.size}x{sp.size}; Diff: {sp.difficulty}\ncalc_time: {sp.calculation_time}ms; total_time: {total_time}s')
    board2text(sp, output='boards.txt')
print('done')

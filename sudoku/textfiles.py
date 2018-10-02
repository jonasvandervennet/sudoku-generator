from sudoku.sudoku import Sudoku
from sudoku.sudokupuzzle import SudokuPuzzle

"""
Sudoku to and from textfiles
"""

def sudoku2text(sudoku, output='sudoku.txt'):
    to_encode = sudoku.get_all_rows()
    print(to_encode)
    with open(output, 'a') as opf:
        for row in to_encode:
            for node in row:
                opf.write(node.textfile)
                if node != row[-1]:
                    opf.write(';')
            opf.write('|')
        opf.write('\n')
    return True

def text2sudoku(input='sudoku.txt'):
    with open(input, 'r') as ipf:
        coded_lines = ipf.readlines()
    return True

from sudoku.sudoku import Sudoku
from sudoku.sudokupuzzle import SudokuPuzzle

"""
Sudoku to and from textfiles
"""

def sudoku2text(sudoku, output='sudoku.txt'):
    "Encodes a Sudoku to a textfile"
    to_encode = sudoku.get_all_rows()
    with open(output, 'a') as opf:
        #  Signal this is a regular sudoku, not a board with solution
        opf.write('S|')
        #  Write all data related to nodes
        for row in to_encode:
            for node in row:
                opf.write(node.textfile)
                if node != row[-1]:
                    opf.write(';')
            opf.write('|')
        #  Write extra data (size)
        opf.write(f"S{sudoku.size}")
        opf.write('\n')
    return True

def board2text(sb, output='sudoku.txt'):
    "Encodes a Sudokuboard (with problem and solution + difficulty) to a textfile"
    pass

def text2sudoku(input='sudoku.txt'):
    with open(input, 'r') as ipf:
        coded_lines = ipf.readlines()
    return True

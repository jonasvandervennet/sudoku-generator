from sudoku.sudoku import Sudoku
from sudoku.sudokupuzzle import SudokuPuzzle

"""
Sudoku to and from textfiles
"""

def sudoku_write(sudoku, ofp):
    #  Write all data related to nodes
    to_encode = sudoku.get_all_rows()
    for row in to_encode:
        for node in row:
            ofp.write(node.textfile)
            if node != row[-1]:
                ofp.write(';')
        ofp.write('|')

def sudoku2text(sudoku, output='sudoku.txt'):
    "Encodes a Sudoku to a textfile"
    to_encode = sudoku.get_all_rows()
    with open(output, 'a') as ofp:
        #  Signal this is a regular sudoku, not a board with solution
        ofp.write('S|')
        sudoku_write(sudoku, ofp)
        #  Write extra data (size)
        ofp.write(f"S{sudoku.size}")
        ofp.write('\n')
    return True

def board2text(sb, output='sudoku.txt'):
    "Encodes a Sudokuboard (with problem and solution + difficulty) to a textfile"
    with open(output, 'a') as ofp:
        #  Signal this is a board WITH solution
        ofp.write('B|')
        sudoku_write(sb.original, ofp)
        ofp.write('$')  # Separate the sudokus
        sudoku_write(sb.solution, ofp)
        #  Write extra data (size, difficulty)
        ofp.write(f"S{sb.size}D{sb.difficulty}")
        ofp.write('\n')
    return True
    

def text2sudoku(input='sudoku.txt'):
    with open(input, 'r') as ifp:
        coded_lines = ifp.readlines()
    return True

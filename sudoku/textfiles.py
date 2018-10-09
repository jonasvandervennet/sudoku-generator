import random

from sudoku.sudokupuzzle import SudokuPuzzle


def sudoku_write(sudoku, ofp):
    #  Write all data related to nodes
    to_encode = sudoku.get_all_rows()
    for row in to_encode:
        for node in row:
            ofp.write(node.textfile)
            if node != row[-1]:
                ofp.write(';')
        ofp.write('|')


def puzzle2text(sb, filename='boards.txt'):
    "Encodes a Sudokuboard (with problem and solution + difficulty) to a textfile"
    with open(filename, 'a') as ofp:
        #  Signal this is a board WITH solution
        ofp.write('B|')
        sudoku_write(sb.original, ofp)
        ofp.write('$|')  # Separate the sudokus
        sudoku_write(sb.solution, ofp)
        #  Write extra data (size, difficulty)
        ofp.write(f"S{sb.size}D{sb.difficulty}")
        ofp.write('\n')
    return True
    

def text2puzzle(filename='boards.txt', index=None):
    with open(filename, 'r') as ifp:
        coded_lines = ifp.readlines()
        selection = random.choice(coded_lines) if index is None else coded_lines[index]
    details = selection.split('|')
    meta = details[-1]
    size = int(meta.split('D')[0].split('S')[-1])
    if not details[size + 1] == '$':
        raise ValueError('Content was not formatted right!')
    custom_input = [[int(coded_node.split(',')[2]) for coded_node in coded_row.split(';')] for coded_row in details[1:size + 1]]
    return SudokuPuzzle(size=size, custom=custom_input)


def show_errors_in_file(filename='boards.txt'):
    with open(filename, 'r') as ifp:
        lines = ifp.readlines()
    error_lines = []
    for i, line in enumerate(lines):
        details = line.split('|')
        meta = details[-1]
        size = int(meta.split('D')[0].split('S')[-1])
        if not details[size + 1] == '$':
            raise ValueError('Content was not formatted right!')
        custom_input = [[int(coded_node.split(',')[2]) for coded_node in coded_row.split(';')] for coded_row in details[1:size + 1]]
        puzzle = SudokuPuzzle(size=size, custom=custom_input)
        if not puzzle.original.is_unique:
            error_lines.append(i + 1)
    if len(error_lines) == 0:
        print('All fine!')
    return error_lines

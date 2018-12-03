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


def puzzle2text(sp, filename='boards.txt'):
    "Encodes a Sudokuboard (with problem and solution + difficulty) to a textfile"
    with open(filename, 'a') as ofp:
        #  Signal this is a board WITH solution
        ofp.write('B|')
        sudoku_write(sp.original, ofp)
        ofp.write('$|')  # Separate the sudokus
        sudoku_write(sp.solution, ofp)
        #  Write extra data (size, difficulty)
        ofp.write(f"S{sp.size}D{sp.difficulty}")
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
    custom_input = [[int(valuestring) for valuestring in coded_row.split(';')] for coded_row in details[1:size + 1]]
    return SudokuPuzzle(size=size, custom=custom_input)


def show_errors_in_file(filename='boards.txt'):
    with open(filename, 'r') as ifp:
        lines = ifp.readlines()
    error_lines = []
    length = len(lines)
    for i in range(length):
        puzzle = text2puzzle(filename=filename, index=i)
        if not puzzle.original.is_unique:
            error_lines.append(i + 1)
    if len(error_lines) == 0:
        return f'Checked file "{filename}". All fine!'
    return error_lines

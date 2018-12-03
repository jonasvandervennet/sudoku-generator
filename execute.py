import os
import time
from multiprocessing.dummy import Pool as ThreadPool

from sudoku.sudokupuzzle import SudokuPuzzle
from sudoku.textfiles import puzzle2text, show_errors_in_file


def fill_file(runs, filename='boards.txt'):
    if isinstance(runs, list):
        runs, filename, index = runs
        print(f'Started thread {index}')
    else:
        index = None
    
    for i in range(runs):
        total_start = time.time()
        sp = SudokuPuzzle(size=9, verbose=False, _diff=175)
        total_time = time.time() - total_start
        # print(f'Size: {sp.size}x{sp.size}; Diff: {sp.difficulty}\ncalc_time: {sp.calculation_time}ms; total_time: {total_time}s')
        if index is not None:
            print(f'{i+1} (thread {index}) time: {total_time}s')
        else:
            print(f'({i+1})time: {total_time}s')
        puzzle2text(sp, filename=filename)
    print('done')


def create_pool(amount=10, sudokus=1000, destination='boards.txt'):
    mapping = [[sudokus, f'.boards{i+1}.txt', i + 1] for i in range(amount)]
    # Make the Pool of workers
    pool = ThreadPool(amount)
    
    results = pool.imap(fill_file, mapping)
    # close the pool and wait for the work to finish
    pool.close()
    pool.join()
    print(results)

    print('Saving results')
    for i in range(amount):
        filename = f'.boards{i+1}.txt'
        with open(filename, 'r') as infile:
            data = infile.readlines()
        os.remove(filename)
        with open(destination, 'a') as outfile:
            for line in data:
                outfile.write(line)
    print('Done creating and saving sudokus')


start = time.time()
# create_pool(amount=10, sudokus=10, destination='boards.txt')
fill_file(10000)
print('Verifying created sudokus...')
print(show_errors_in_file())
print(f'Completion in {time.time() - start} seconds')

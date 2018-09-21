import numpy as np
import random
import time


class Sudoku():
    def __init__(self, size=9, custom=None, verbose=False):
        # assume size is perfect square (TODO: assert square)
        # size is defined as the length of one side
        """
        Custom should be a list of lists containing each row of the sudoku.
        Empty spots should be represented by a 0.
        """
        self.verbose = verbose
        self.size = size
        self._tilesize = int(np.sqrt(size))
        self.nodes, self._rows, self._cols, self._tiles = self.initnodes()
        self.connect_nodes()
        self.fillgrid(custom)

    def get_row(self, row):
        return self._rows[row]

    def get_col(self, col):
        return self._cols[col]

    def get_tile(self, tile):
        return self._tiles[tile]

    def initnodes(self):
        nodes, rows, cols, tiles = [], [[] for _ in range(self.size)], [[] for _ in range(self.size)], [[] for _ in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                node = Node(row, col)
                nodes.append(node)
                rows[row].append(node)
                cols[col].append(node)
                #  Tiles are for example the 3*3 squares in default sudoku
                tilenr = self.calculate_tile(row, col)
                tiles[tilenr].append(node)
        return nodes, rows, cols, tiles

    def calculate_tile(self, row, col):
        tilerow = row // self._tilesize
        tilecol = col // self._tilesize
        return tilerow * self._tilesize + tilecol

    def connect_nodes(self):
        for node in self.nodes:
            for connected_node in self.get_row(node.row) + self.get_col(node.col) + self.get_tile(self.calculate_tile(node.row, node.col)):
                node.connected_nodes.add(connected_node)
            node.connected_nodes -= set([node])

    def fillgrid(self, custom=None):
        def executeFill(queue, depth=0):
            if depth % 50 == 0:
                self.print(f'On rec depth {depth}')
                self.print(self)

            node = queue[0]
            queue.pop(0)  # ~pop front

            neighbor_values = set()
            for cell in node.connected_nodes:
                neighbor_values.add(cell.value)

            options = list(set([i for i in range(1, self.size + 1)]) - neighbor_values)
            random.shuffle(options)

            for option in options:
                node.value = option

                if len(queue) == 0:  # empty
                    return True, queue

                result, queue = executeFill(queue, depth=depth + 1)
                if result:
                    return True, queue

            # base case
            node.value = 0
            queue = [node] + queue  # ~push front
            return False, queue

        if custom is not None:
            try:
                for i, row in enumerate(self._rows):
                    for j, node in enumerate(row):
                        if custom[i][j] != 0:
                            node.original = True
                        node.value = custom[i][j]
            except IndexError:
                raise IndexError("Custom sudoku layout was not of the right format!")
            except Exception as e:  # replace with indexoutofboundserror
                raise e

            self.print("Custom input submitted and processed:")
            self.print(self)

        queue = [node for node in self.nodes if not node.original]
        if len(queue) == 0:
            #  The custom input was completely full, check if valid or not
            if not self.is_valid:
                self.print("Given solution is not valid!")
                self.print(self)
                return False
            else:
                self.print("Success! Given solution was valid!")
                self.print(self)
                return True

        self.print('Trying to fill board...')
        starttime = time.time()
        if (not executeFill(queue)[0]) or (not self.is_valid):
            self.print("Unable to fill board!")
            raise Exception("Unable to fill board!")
        else:
            self.print("Filled board!")
            self.print(f"\nSolution:\n{self}")
            interval = time.time() - starttime
            self.calculation_time = interval
            self.print(f"Solution found in {interval}s")

    @property
    def is_valid(self):
        for node in self.nodes:
            if not node.is_valid:
                return False
        return True

    def print(self, msg):
        if self.verbose:
            print(msg)

    def __str__(self):
        result = ""
        for row in self._rows:
            result += str([node.value for node in row]) + '\n'
        return result


class Node():
    def __init__(self, row, col, original=False):
        self.row = row
        self.col = col
        self.value = 0
        self.original = original
        self.connected_nodes = set()

    @property
    def is_valid(self):
        if self.value == 0:
            return False
        for node in self.connected_nodes:
            if node.value == self.value:
                return False
        return True

    def __str__(self):
        return f"node({self.row},{self.col})"


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


# sc = Sudoku(size=9, custom=custom_expert, verbose=True)
# s16 = Sudoku(size=16, verbose=True)
# s16c = Sudoku(size=16, custom=custom_16, verbose=True)
# s25 = Sudoku(size=25, verbose=True)
makelist([5] * 15, verbose=True)

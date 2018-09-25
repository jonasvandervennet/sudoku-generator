import numpy as np
import random
import time


class Sudoku():
    def __init__(self, size=9, custom=None, solve=False, verbose=False):
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
        if custom is not None:
            self.fillgrid(custom)
        if solve:
            self.solve()

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

    def fillgrid(self, custom):
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

    def solve(self):
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

        queue = [node for node in self.nodes if not node.original]
        if len(queue) == 0:
            #  The sudoku was already completely full, check if valid or not
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
        return self

    @property
    def is_valid(self):
        for node in self.nodes:
            if not node.is_valid:
                return False
        return True

    def print(self, msg):
        if self.verbose:
            print(msg)

    def equals(self, other):
        try:
            for i, row in enumerate(self._rows):
                for j, node in enumerate(row):
                    if not node._equals(other.get_row(i)[j]):
                        return False
        except Exception:
            return False
        return True

    def __eq__(self, other):
        if not isinstance(other, Sudoku):
            return False
        return self.equals(other)
    
    def __ne__(self, other):
        if not isinstance(other, Sudoku):
            return False
        return not self.equals(other)

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

    def _equals(self, other):
        return (self.value, self.row, self.col) == (other.value, other.row, other.col)

    def __str__(self):
        return f"node({self.row},{self.col}): {self.value}"

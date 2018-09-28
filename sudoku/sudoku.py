import numpy as np
import random
import time

from sudoku.node import Node


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
        if custom is not None:
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

    def fillgrid(self, custom):
        try:
            for i, row in enumerate(self._rows):
                for j, node in enumerate(row):
                    if custom[i][j] != 0:
                        node.original = True
                    node.value = custom[i][j]
        except IndexError:
            raise IndexError("Custom sudoku layout was not of the right format!")
        except Exception as e:  # Other error, just raise
            raise e

        self.print("Custom input submitted and processed:")
        self.print(self)

    def solve(self, returnBranching=False):
        """
        Returns a new sudoku containing the solution of the given sudoku.
        """
        to_solve = self.copy()

        def executeFill(queue, depth=0):
            if depth % 50 == 0 and depth != 0:
                to_solve.print(f'On rec depth {depth}')
                to_solve.print(to_solve)

            node = queue[0]
            queue.pop(0)  # ~pop front

            options = list(set([i for i in range(1, to_solve.size + 1)]) - node.get_neighbor_values())
            random.shuffle(options)
            branch = 1  # for detetermining branch factor (difficulty)
            for option in options:
                node.value = option

                if len(queue) == 0:  # empty
                    return {'result': True, 'queue': queue, 'branchfactor': branch}

                results = executeFill(queue, depth=depth + 1)
                queue = results['queue']
                if results['result']:
                    branch = (branch - 1)**2
                    branch += results['branchfactor']  # keeping summation going
                    return {'result': True, 'queue': queue, 'branchfactor': branch}
                branch += 1

            # base case
            node.value = 0
            queue = [node] + queue  # ~push front
            return {'result': False, 'queue': queue}
        
        queue = [node for node in to_solve.nodes if not node.original]
        if len(queue) == 0:
            #  The sudoku was already completely full, check if valid or not
            if not to_solve.is_valid:
                to_solve.print("Given solution is not valid!")
                to_solve.print(to_solve)
                return False
            else:
                to_solve.print("Success! Given solution was valid!")
                to_solve.print(to_solve)
                return True

        to_solve.print('Trying to fill board...')
        starttime = time.time()
        executionResults = executeFill(queue)
        interval = time.time() - starttime
        to_solve.calculation_time = interval / 1000  # Calc_time in ms
        if (not executionResults['result']) or (not to_solve.is_valid):
            to_solve.print("Unable to fill board!")
            raise Exception("Unable to fill board!")
        else:  # Successfully filled the board!
            branchingFactor = executionResults.get('branchfactor', None)
            to_solve.print("Filled board!")
            to_solve.print(f"\nSolution:\n{to_solve}")
            to_solve.print(f"Solution found in {interval}s")
        if returnBranching:
            return to_solve, branchingFactor
        return to_solve

    @property
    def empty(self):
        empty = 0
        for node in self.nodes:
            if node.value == 0:
                empty += 1
        self.print(f'{empty} empty values')
        return empty

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
    
    def copy(self):
        """
        Returns new sudoku instance with new nodes containing the same values.
        """
        custom_input = [[node.value for node in row] for row in self._rows]
        self.print('Copying data into new Sudoku.')
        newSudoku = Sudoku(size=self.size, custom=custom_input, verbose=self.verbose)
        self.print('Verifying data of new Sudoku.')
        # Check for original
        for node in self.nodes:
            for newnode in newSudoku.nodes:
                if node._equals(newnode):
                    newnode.original = node.original
        self.print('Data verified.\n')
        return newSudoku

    def get_options(self, node):
        return list(set([i for i in range(1, self.size + 1)]) - node.get_neighbor_values())
    
    def __str__(self):
        result = ""
        for row in self._rows:
            result += str([node.value for node in row]) + '\n'
        return result

    def solve_smart(self, returnBranching=False):
        to_solve = self.copy()

        def gather_best_node(sudoku):
            """
            Searches nodes with least amount of options, selects one randomly
            """

            best_nodes = []
            current_min_options = sudoku.size

            # Gather a list of nodes with the least
            for node in sudoku.nodes:
                if not node.value == 0:
                    continue
                options = sudoku.get_options(node)
                if len(options) < current_min_options:
                    # New best node found
                    best_nodes = [node]
                    current_min_options = len(options)
                elif len(options) == current_min_options:
                    best_nodes.append(node)
            return random.choice(best_nodes) if len(best_nodes) != 0 else None
        
        def executeFill(depth=0):
            if depth % 50 == 0 and depth != 0:
                to_solve.print(f'On rec depth {depth}')
                to_solve.print(to_solve)

            node = gather_best_node(to_solve)
            if node is None:
                return {'result': True, 'branchfactor': 1}
            options = to_solve.get_options(node)
            random.shuffle(options)

            branch = 1  # for detetermining branch factor (difficulty)
            for option in options:
                node.value = option

                results = executeFill(depth=depth + 1)
                if results['result']:
                    branch = (branch - 1)**2
                    branch += results['branchfactor']  # keeping summation going
                    return {'result': True, 'branchfactor': branch}
                branch += 1

            # base case
            node.value = 0
            return {'result': False}
        
        queue = [node for node in to_solve.nodes if not node.original]
        if len(queue) == 0:
            #  The sudoku was already completely full, check if valid or not
            if not to_solve.is_valid:
                to_solve.print("Given solution is not valid!")
                to_solve.print(to_solve)
                return False
            else:
                to_solve.print("Success! Given solution was valid!")
                to_solve.print(to_solve)
                return True

        to_solve.print('Trying to fill board...')
        starttime = time.time()
        executionResults = executeFill()
        interval = time.time() - starttime
        to_solve.calculation_time = interval / 1000  # Calc_time in ms
        if (not executionResults['result']) or (not to_solve.is_valid):
            to_solve.print("Unable to fill board!")
            raise Exception("Unable to fill board!")
        else:  # Successfully filled the board!
            branchingFactor = executionResults.get('branchfactor', None)
            to_solve.print("Filled board!")
            to_solve.print(f"\nSolution:\n{to_solve}")
            to_solve.print(f"Solution found in {interval}s")
        if returnBranching:
            return to_solve, branchingFactor
        return to_solve

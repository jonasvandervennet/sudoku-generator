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
    
    def get_neighbor_values(self):
        """
        Returns a set of values contained in this node's connected nodes
        """
        neighbor_values = set()
        for cell in self.connected_nodes:
            neighbor_values.add(cell.value)
        return neighbor_values

    def equals(self, other):
        if not isinstance(other, Node):
            return False
        return (self.value, self.row, self.col) == (other.value, other.row, other.col)

    @property
    def textfile(self):
        "Node representation when encoded in textfile"
        return f'{self.row},{self.col},{self.value}'

    def __str__(self):
        return f"node({self.row},{self.col}): {self.value}"

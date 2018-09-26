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

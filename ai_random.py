import itertools
import random

class AI(object):
    def __init__(self, cells_per_side=8):
        self.cells_per_side = cells_per_side
        self.cell_indeces = list(itertools.product(range(cells_per_side), range(cells_per_side)))
        self.moves = ['u', 'd', 'l', 'r']

    def think(self, board):
        return random.choice(self.cell_indeces), random.choice(self.moves)

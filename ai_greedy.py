import itertools
import random

import numpy as np

class AI(object):
    def __init__(self, cells_per_side=8, pick_best_prob=.95, only_bottom_prob=0.0, handle_hyper_prob=.00):
        self.handle_hyper_prob = handle_hyper_prob
        self.pick_best_prob = pick_best_prob
        self.only_bottom_prob = only_bottom_prob
        self.cells_per_side = cells_per_side
        self.moves = ['d', 'r']
        self.move_offset = {'u':(0,-1), 'd':(0,1), 'l':(-1,0), 'r':(1,0)}
        self.cell_indeces = list(itertools.product(range(cells_per_side), range(cells_per_side)))
        self.prev = []

    def think(self, board):
        # Try all possible moves, see which produce the most squares in a row
        board = np.array(board)
        # Ignore our last moves on the board
        for x in self.prev:
            board[x[1], x[0]] = None
        good_moves = []
        # Only do bottom
        low = 0
        high = self.cells_per_side
        if random.random() < self.only_bottom_prob:
            low = 3
        for y in range(low, high):
            for x in range(self.cells_per_side):
                if board[y][x] == None:
                    continue
                for move in self.moves:
                    try:
                        score = self._match(x, y, move, board)
                    except IndexError:
                        continue
                    # Handle hypercube
                    if random.random() < self.handle_hyper_prob and board[y][x] == 'h':
                        score = 4
                    if score >= 3:
                        good_moves.append((score, (x, y, move)))
        if not len(good_moves):
            self.prev = []
            return None
        if random.random() < self.pick_best_prob:
            #print('good')
            good_moves.sort(lambda x,y: cmp(x[0], y[0]), reverse=True)
            best_score = good_moves[0][0]
            #good_moves = [(x[1][1], x[1]) for x in good_moves if x[0] == best_score]
            good_moves = [x for x in good_moves if x[0] == best_score]
            #good_moves.sort(lambda x,y: cmp(x[0], y[0]), reverse=True)
            score, xymove = random.choice(good_moves)
            #score, xymove = good_moves[0]
        else:
            #print('randRand')
            score, xymove = random.choice(good_moves)
        self._set_prev(xymove)
        return xymove[0:2], xymove[2]

    def _set_prev(self, xymove, max_buf=0):
        xp, yp = self._move_xy(*xymove)
        self.prev.append((xp, yp))
        self.prev.append((xymove[0], xymove[1]))
        self.prev = self.prev[0:max_buf]
        
    def _rand_move(self):
        return random.choice(self.cell_indeces), random.choice(self.moves)

    def _move_xy(self, x, y, move):
        off = self.move_offset[move]
        return off[0]+x, off[1]+y

    def _flip(self, board, x, y, xp, yp):
        t = board[y][x]
        board[y][x] = board[yp][xp]
        board[yp][xp] = t
    
    def _row_match(self, row, board):
        try:
            return max([len(list(x[1])) for x in itertools.groupby(board[row,:]) if x[0] != None])
        except ValueError:
            return 0

    def _col_match(self, col, board):
        try:
            return max([len(list(x[1])) for x in itertools.groupby(board[:,col]) if x[0] != None])
        except ValueError:
            return 0
            
    def _match(self, x, y, move, board):
        xp, yp = self._move_xy(x, y, move)
        # Flip the values around
        self._flip(board, x, y, xp, yp)
        xs = np.unique((x, xp))
        ys = np.unique((y, yp))
        val = max([self._col_match(i, board) for i in xs]+[self._row_match(i, board) for i in ys])
        self._flip(board, x, y, xp, yp)
        return val

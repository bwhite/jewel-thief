"""
ScreenParser is a class that takes in a PIL image with the "parse" method, and retuturns a 2D array (as nested python lists) representing the playing board.  A single letter will represent unique colors, a None value represents unknown values.
"""
import itertools

import numpy as np
import Image
import ImageFilter

class ScreenParser(object):
  def __init__(self, offset=(410., 304.), width=40., cells_per_side=8):# Also 390, 304
    # Store parameters
    self.offset = np.array(offset)
    self.width = width
    self.cells_per_side = cells_per_side
    # Build internal representation
    self.cell_center_offset = np.array([width/2.]*2)
    self.cell_indeces = itertools.product(range(cells_per_side), range(cells_per_side))
    self.cells = list(self.cell_indeces)
    def make_center(cell):
      return np.round(np.array(cell) * width  + self.cell_center_offset + self.offset)
    self.cells = map(make_center, self.cells)
    # Setup color chart
    self.color_chart = [('g', [29., 180., 57.]),
                        ('g', [35., 151., 37.]),
                        ('r', [248., 27., 54.]),
                        ('r', [191., 46., 55.]),
                        ('b', [22., 123., 232.]),
                        ('b', [159., 190., 208.]),
                        ('b', [48., 125., 186.]),
                        ('w', [255., 255., 255.]),
                        ('w', [177.,  177.,  177.]),
                        ('p', [235, 34., 229.]),
                        ('p', [202., 162., 200.]),
                        ('y', [252., 244., 38.]),
                        ('y', [194., 198., 42.]),
                        ('o', [221., 137., 51.]),
                        ('o', [204., 182., 158.])]
    self.color_chart = [(color[0], np.array(color[1]))
                        for color in self.color_chart]
    # Setup movement offsets
    self.move_offset = (('l',(-self.width, 0.0)),
                        ('r',(self.width, 0.0)),
                        ('u',(0.0, -self.width)),
                        ('d',(0.0, self.width)))
    self.move_offset = dict([(move[0], np.array(move[1]))
                             for move in self.move_offset])

  def parse(self, image):
    board = [self._classify(image.getpixel(tuple(cell))) for cell in self.cells]
    return np.array(board).reshape((self.cells_per_side, self.cells_per_side)).T.tolist()

  def train(self, image):
    board = np.array(self.parse(image))
    board = [(self._classify(image.getpixel(tuple(cell))), image.getpixel(tuple(cell))) for cell in self.cells]
    vals = {}
    for n, v in board:
      try:
        vals[n].append(v)
      except KeyError:
        vals[n] = [v]
    return [(val[0], np.mean(val[1], 0)) for val in vals.iteritems()]

  def cell_index_to_cell(self, cell_index):
    return self.cells[cell_index[0]*self.cells_per_side + cell_index[1]]

  def _classify(self, pixel, max_val=45.):
    pixel = np.array(pixel)
    dists = [np.linalg.norm(pixel - color[1]) for color in self.color_chart]
    ind = np.argmin(dists)
    out = self.color_chart[ind][0]
    if dists[ind] > max_val:
      out = None
    #print(dists[ind])
    return out

if __name__ == "__main__":
  import time
  import sys
  a = time.time()
  sp = ScreenParser()
  if len(sys.argv) > 1:
    image = Image.open(sys.argv[1])
  else:
    image = Image.open('out.jpg')
  image = image.resize((image.size[0]/2, image.size[1]/2))
  image = image.filter(ImageFilter.SMOOTH)
  image = image.resize((image.size[0]*2, image.size[1]*2))
  image.save('out_parse_smooth.jpg')
  board = np.array(sp.parse(image))
  print(board)
  print(time.time()-a)
  print(sp.train(image))
  probe = (3, 1)
  probe_pix = tuple(sp.cells[probe[0]*8+probe[1]])
  probe_val = image.getpixel(probe_pix)
  print(probe)
  print(probe_pix)
  print(probe_val)
  

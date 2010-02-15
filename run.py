import time
import random

import numpy as np
import Image
import ImageFilter

import screenshot
import screen_parser
import mouse
from ai_greedy import AI

if __name__ == "__main__":
    image = screenshot.get_screenshot()
    #image = Image.open('e0.jpg')
    sp = screen_parser.ScreenParser()
    print(np.array(sp.cells).T)
    ai = AI()
    while 1:
        image = screenshot.get_screenshot()
        image = image.resize((image.size[0]/2, image.size[1]/2))
        image = image.filter(ImageFilter.SMOOTH)
        image = image.resize((image.size[0]*2, image.size[1]*2))
        board = sp.parse(image)
        if random.random() < .5:
            bad_spots = len([x for x in np.array(board).ravel() if x == None or x == 'w'])
            if bad_spots > 30:
                mouse.move_click((490,575))
                time.sleep(.1)
                mouse.move_click((910,298))
                time.sleep(.5)
                print('bad')
        try:
            cell_index, move = ai.think(board)
        except TypeError:
            continue
        from_move = sp.cell_index_to_cell(cell_index)
        to_move = sp.move_offset[move] + from_move
        mouse.drag(from_move, to_move)
        #mouse.hide()
        time.sleep(.05)
        #time.sleep(.2)

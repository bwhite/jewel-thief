"""
Provides the following mouse functionality.
move(loc): Where loc = (x, y)
down and up
click: An up and a down
drag: Used for specify two points to click and drag to.
"""
import subprocess

def _rp(cmd):
    subprocess.call(cmd.split())

def move(loc):
    _rp('xdotool mousemove %d %d'%(loc[0], loc[1]))

def hide():
    move((0,300))

def click():
    _rp('xdotool click 1')

def move_click(loc):
    move(loc)
    click()

def down():
    _rp('xdotool mousedown 1')

def up():
    _rp('xdotool mouseup 1')

def drag(loc0, loc1):
    move(loc0)
    down()
    move(loc1)
    up()

if __name__ == '__main__':
    import time
    a = time.time()
    drag((200, 200), (300, 300))
    print(time.time()-a)

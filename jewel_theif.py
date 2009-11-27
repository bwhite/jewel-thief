import subprocess

def make_screenshot(fn='out.jpg'):
    subprocess.Popen('scrot %s'%(fn).split()).wait()

def main():
    while 1:
        # Take screenshot
        make_screenshot()
        # Load image
        # Find board positions
        # Make moves
        break
        

if name == "__main__":
    main()

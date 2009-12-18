"""
Provides a method get_screenshot() that will take a full screenshot and return it as a PIL image.
"""

import gtk
import Image

def get_screenshot():
  try:
    img_width = gtk.gdk.screen_width()
    img_height = gtk.gdk.screen_height()
    screengrab = gtk.gdk.Pixbuf(
      gtk.gdk.COLORSPACE_RGB,
      False,
      8,
      img_width,
      img_height
      )
    screengrab.get_from_drawable(
      gtk.gdk.get_default_root_window(),
      gtk.gdk.colormap_get_system(),
      0, 0, 0, 0,
      img_width,
      img_height
    )
  except Exception, e:
    print "Failed taking screenshot"
    exit()
  final_screengrab = Image.frombuffer(
    "RGB",
    (img_width, img_height),
    screengrab.get_pixels(),
    "raw",
    "RGB",
    screengrab.get_rowstride(),
    1
  )
  return final_screengrab

if __name__ == "__main__":
  import time
  time.sleep(2)
  b = time.time()
  a = get_screenshot()
  print(time.time()-b)  
  a.save('out.jpg')

# Card animation I made
from math import pi, sin, cos, sqrt
from time import sleep
# from dispTBase import *

width = 240
height = 240

from PIL import Image, ImageDraw, ImageFont

# The newest version of Pillow forced x1 <= x2 for no good reason and I'm pissed it broke evyerthing. 
# I copied this block from the web so this would boot. I shouldnt need it, but I do
_old_rect = ImageDraw.ImageDraw.rectangle
def _safe_rect(self, xy, *a, **kw):
    x0, y0, x1, y1 = xy
    if x1 < x0: x0, x1 = x1, x0
    if y1 < y0: y0, y1 = y1, y0
    return _old_rect(self, (x0, y0, x1, y1), *a, **kw)
ImageDraw.ImageDraw.rectangle = _safe_rect

image = Image.new("RGB", (width, height), (255, 255, 255))
draw = ImageDraw.Draw(image)

#origin = 120 long and 90 tall
"""
    x1 = 120 - 31.25
    y1 = 90 - 43.75
    x2 = 120 + 31.25
    y2 = 90 + 43.75
"""
orX = 120
orY = 90
x = 31.25
y = 43.75
x2 = x - 5
y2 = y - 5
z = 5
t = 30

def spin(var, t, inc):
    return(var * cos((pi / 2) * (inc / t)))

def doSpin(times):
    count = 0
    for _ in range(times):
        for inc in range(t):
            oAY = orY + (orY * 0.35 * -cos((pi * (inc)) / (2 * (t))))
            draw.rectangle((0, 0, width, height), fill = (0, 0, 0))
            draw.rectangle((0, 0, width, 180), fill = (92, 155, 51))
            draw.rectangle((orX - spin(x, t, t - inc), oAY - y, orX + spin(x, t, t - inc), oAY + y), fill = (255, 255, 255))
            draw.rectangle((orX - spin(x2, t, t - inc), oAY - y + 5, orX + spin(x2, t, t - inc), oAY + y - 5), fill = (100, 0, 0))

            # disp.image(image)
            # if count % 5 and count <= 50:
            #     image.show()
            # count += 1
            sleep(0.01)

        for inc in range(t):
            oAY = orY + (orY * 0.35 * -cos((pi * (t + inc)) / (2 * (t))))
            draw.rectangle((0, 0, width, height), fill = (0, 0, 0))
            draw.rectangle((0, 0, width, 180), fill = (92, 155, 51))
            draw.rectangle((orX - spin(x, t, inc), oAY - y, orX + spin(x, t, inc), oAY + y), fill = (255, 255, 255))
            draw.rectangle((orX - spin(x2, t, inc), oAY - y + 5, orX + spin(x2, t, inc), oAY + y - 5), fill = (100, 0, 0))

            # disp.image(image)
            # if count % 5 and count <= 50:
            #     image.show()
            # count += 1            
            sleep(0.01)

        #second side
        for inc in range(t):
            oAY = orY + (orY * 0.35 * -cos((pi * (2 * t + inc)) / (2 * (t))))
            draw.rectangle((0, 0, width, height), fill = (0, 0, 0))
            draw.rectangle((0, 0, width, 180), fill = (92, 155, 51))
            draw.rectangle((orX - spin(x, t, t - inc), oAY - y, orX + spin(x, t, t - inc), oAY + y), fill = (255, 255, 255))
            draw.polygon(((orX, oAY - 10), (orX - spin(10, t, t - inc), oAY), (orX, oAY + 10), (orX + spin(10, t, t - inc), oAY)), fill = (100, 0, 0))

            draw.polygon(((orX - spin(x, t, t - inc) + spin(12.5, t, t - inc), oAY - 38.75), (orX - spin(x, t, t - inc) + spin(20, t, t - inc), oAY - 18.75), (orX - spin(x, t, t - inc) + spin(5, t, t - inc), oAY - 18.75)), fill = (100, 0, 0))
            draw.polygon(((orX - spin(x, t, t - inc) + spin(12.5, t, t - inc), oAY - 32.75), (orX - spin(x, t, t - inc) + spin(17.75, t, t - inc), oAY - 18.75), (orX - spin(x, t, t - inc) + spin(7.25, t, t - inc), oAY - 18.75)), fill = (255, 255, 255))  
            draw.rectangle((orX - spin(x, t, t - inc) + spin(8.75, t, t - inc), oAY - 28, orX - spin(x, t, t - inc) + spin(16.25, t, t - inc), oAY - 28 + sqrt((4 ** 2) - (3.4 ** 2))), fill = (100, 0, 0))

            draw.polygon(((orX + spin(x, t, t - inc) - spin(12.5, t, t - inc), oAY + 38.75), (orX + spin(x, t, t - inc) - spin(20, t, t - inc), oAY + 18.75), (orX + spin(x, t, t- inc) - spin(5, t, t - inc), oAY + 18.75)), fill = (100, 0, 0))
            draw.polygon(((orX + spin(x, t, t - inc) - spin(12.5, t, t - inc), oAY + 32.75), (orX + spin(x, t, t - inc) - spin(17.75, t, t - inc), oAY + 18.75), (orX + spin(x, t, t - inc) - spin(7.25, t, t - inc), oAY + 18.75)), fill = (255, 255, 255))
            draw.rectangle((orX + spin(x, t, t - inc) - spin(8.75, t, t - inc), oAY + 28, orX + spin(x, t, t - inc) - spin(16.25, t, t - inc), oAY + 28 - sqrt((4 ** 2) - (3.4 ** 2))), fill = (100, 0, 0))
            # disp.image(image)
            # if count % 1 and count <= 10:
            #     image.show()
            # count += 1
            sleep(0.01)

        for inc in range(t):
            oAY = orY + (orY * 0.35 * -cos((pi * (3 * t + inc)) / (2 * (t))))
            draw.rectangle((0, 0, width, height), fill = (0, 0, 0))
            draw.rectangle((0, 0, width, 180), fill = (92, 155, 51))
            draw.rectangle((orX - spin(x, t, inc), oAY - y, orX + spin(x, t, inc), oAY + y), fill = (255, 255, 255))
            draw.polygon(((orX, oAY - 10), (orX - spin(10, t, inc), oAY), (orX, oAY + 10), (orX + spin(10, t, inc), oAY)), fill = (100, 0, 0))

            draw.polygon(((orX - spin(x, t, inc) + spin(12.5, t, inc), oAY - 38.75), (orX - spin(x, t, inc) + spin(20, t, inc), oAY - 18.75), (orX - spin(x, t, inc) + spin(5, t, inc), oAY - 18.75)), fill = (100, 0, 0))
            draw.polygon(((orX - spin(x, t, inc) + spin(12.5, t, inc), oAY - 32.75), (orX - spin(x, t, inc) + spin(17.75, t, inc), oAY - 18.75), (orX - spin(x, t, inc) + spin(7.25, t, inc), oAY - 18.75)), fill = (255, 255, 255))  
            draw.rectangle((orX - spin(x, t, inc) + spin(8.75, t, inc), oAY - 28, orX - spin(x, t, inc) + spin(16.25, t, inc), oAY - 28 + sqrt((4 ** 2) - (3.4 ** 2))), fill = (100, 0, 0))

            draw.polygon(((orX + spin(x, t, inc) - spin(12.5, t, inc), oAY + 38.75), (orX + spin(x, t, inc) - spin(20, t, inc), oAY + 18.75), (orX + spin(x, t, inc) - spin(5, t, inc), oAY + 18.75)), fill = (100, 0, 0))
            draw.polygon(((orX + spin(x, t, inc) - spin(12.5, t, inc), oAY + 32.75), (orX + spin(x, t, inc) - spin(17.75, t, inc), oAY + 18.75), (orX + spin(x, t, inc) - spin(7.25, t, inc), oAY + 18.75)), fill = (255, 255, 255))
            draw.rectangle((orX + spin(x, t, inc) - spin(8.75, t, inc), oAY + 28, orX + spin(x, t, inc) - spin(16.25, t, inc), oAY + 28 - sqrt((4 ** 2) - (3.4 ** 2))), fill = (100, 0, 0))
            # disp.image(image)
            if count <= 15:
                image.show()
            count += 1
            sleep(0.01)

if __name__ == "__main__":
    print("launched")
    doSpin(1)

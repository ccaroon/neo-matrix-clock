import time
import random
from machine import Pin
from neopixel import NeoPixel

pin_num = 15

# Number of Pixel in board/strip/matrix
num_pixels = 40

# RGB == 3 | RGBW == 4
bits_per_pixel = 4

pin = Pin(pin_num, Pin.OUT)
np = NeoPixel(pin, num_pixels, bpp=bits_per_pixel)

def matrix():
    for i in range(0, num_pixels):
        color = random.choice(((0,0,0,0),(0,0,128,0)))
        np[i] = color

    np.write()
# -----------------------------------------------------------------------------
while True:
    matrix()
    time.sleep(0.5)

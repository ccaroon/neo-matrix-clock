import random
from machine import Pin
from neopixel import NeoPixel

class NeoMatrix:
    PIN = 15
    PIXELS = 40

    def __init__(self):
        pin = Pin(self.PIN, Pin.OUT)
        # RGBW, so bpp=4
        self.__matrix = NeoPixel(pin, self.PIXELS, bpp=4)

    def random_fill(self):
        for i in range(0,self.PIXELS):
            red = random.randint(0,255)
            green = random.randint(0,255)
            blue = random.randint(0,255)
            white = random.randint(0,32)

            self.__matrix[i] = (red, green, blue, white)

        self.__matrix.write()

    def matrix(self):
        for i in range(0, self.PIXELS):
            color = random.choice(((0,0,0,0),(0,32,0,0)))
            self.__matrix[i] = color

        self.__matrix.write()

    def set(self, num, color):
        self.__matrix[num] = color.as_tuple()

    def set_rc(self, row, col, color):
        num = (row * 8) + col
        self.set(num, color)

    def update(self):
        self.__matrix.write()

import random
import time

from machine import Pin
from neopixel import NeoPixel

from lib.colors.color_factory import ColorFactory

class NeoMatrix:
    PIN = 15
    PIXELS = 40
    OFF = ColorFactory.get("black")

    def __init__(self, rgbw=False):
        pin = Pin(self.PIN, Pin.OUT)

        bpp = 4 if rgbw else 3
        self.__matrix = NeoPixel(pin, self.PIXELS, bpp=bpp)
        self.__rgbw = rgbw

    def __row_col_to_num(self, row, col):
        return (row * 8) + col

    def clear(self):
        self.fill(self.OFF)

    def fill(self, color):
        self.__matrix.fill(color.as_tuple(self.__rgbw))
        self.__matrix.write()

    def slow_fill(self, color, delay=0.5):
        self.clear()

        # fill slowly in reverse order
        for i in range(self.PIXELS-1, -1, -1):
            self.__matrix[i] = color.as_tuple(self.__rgbw)
            self.__matrix.write()
            time.sleep(delay)

    # Walk each pixel
    def test(self, color=None, iterations=1, delay=0.25):
        for _ in range(iterations):
            self.clear()

            test_color = ColorFactory.random() if color is None else color

            for i in range(0, self.PIXELS):
                if i > 0:
                    self.__matrix[i-1] = ColorFactory.get("black").as_tuple(self.__rgbw)

                self.__matrix[i] = test_color.as_tuple(self.__rgbw)

                self.__matrix.write()
                time.sleep(delay)

    # Walk each row
    def test2(self, color=None, iterations=1, delay=0.25):
        self.clear()

        for _ in range(iterations):
            test_color = ColorFactory.random() if color is None else color
            for row in range(0,5):

                if row > 0:
                    for col in range(0,8):
                        self.set_rc(row-1, col, ColorFactory.get("black"))

                for col in range(0,8):
                    self.set_rc(row, col, test_color)

                self.update()
                time.sleep(delay)

    def twinkle(self, color, delay=0.5):
        self.clear()

        while True:
            num = random.randint(0,self.PIXELS - 1)

            self.__matrix[num] = color.as_tuple(self.__rgbw)
            self.__matrix.write()

            time.sleep(delay)

            self.__matrix[num] = self.OFF.as_tuple(self.__rgbw)
            self.__matrix.write()

    def random_fill(self):
        for i in range(0,self.PIXELS):
            color = ColorFactory.random()

            self.__matrix[i] = color.as_tuple(self.__rgbw)

        self.__matrix.write()

    def set(self, num, color):
        self.__matrix[num] = color.as_tuple(self.__rgbw)

    def set_rc(self, row, col, color):
        num = self.__row_col_to_num(row, col)
        self.set(num, color)

    def draw_glyph(self, glyph, color, **kwargs):
        color2 = kwargs.get("color2", self.OFF)
        row_offset = kwargs.get("row_offset", 0)
        col_offset = kwargs.get("col_offset", 0)

        for px in glyph:
            px_color = color2
            if px["on"]:
                px_color = color

            # TODO: Handle index-out-of-range for row & col
            self.set_rc(px["row"]+row_offset, px["col"]+col_offset, px_color)

    def toggle(self, num, color):
        curr_color = self.__matrix[num]
        if curr_color == self.OFF.as_tuple(self.__rgbw):
            self.__matrix[num] = color.as_tuple(self.__rgbw)
        else:
            self.__matrix[num] = self.OFF.as_tuple(self.__rgbw)

    def toggle_rc(self, row, col, color):
        num = self.__row_col_to_num(row, col)
        self.toggle(num, color)

    def invert(self, color=ColorFactory.get("white")):
        for num in range(self.PIXELS):
            self.toggle(num, color)
        self.update()

    def update(self):
        self.__matrix.write()

    def __str__(self):
        return "NeoMatrix(pin=%d,px_count=%d/%d)" % (self.PIN, self.PIXELS, len(self.__matrix))

import random
import time
from machine import Pin

from color_factory import ColorFactory
from neopixel import NeoPixel

class NeoMatrix:
    PIN = 15
    PIXELS = 40
    OFF = (0,0,0,0)

    BAD_PIXELS = (31,)

    def __init__(self):
        pin = Pin(self.PIN, Pin.OUT)
        # RGBW, so bpp=4
        self.__matrix = NeoPixel(pin, self.PIXELS, bpp=4)

    def clear(self):
        self.__matrix.fill(self.OFF)
        self.__matrix.write()

    def fill(self, color):
        self.__matrix.fill(color.as_tuple())
        self.__matrix.write()

    def slow_fill(self, color, delay=0.5):
        # self.clear()

        # fill
        for i in range(self.PIXELS-1, -1, -1):
            if i in self.BAD_PIXELS:
                print("skipping...%d" % (i))
                next

            self.__matrix[i] = color.as_tuple()
            self.__matrix.write()
            time.sleep(delay)

    # Walk each pixel
    def test(self, color=None, iterations=1, delay=0.25):
        for _ in range(iterations):
            self.clear()

            test_color = ColorFactory.random() if color is None else color

            for i in range(0, self.PIXELS):
                if i > 0:
                    self.__matrix[i-1] = ColorFactory.get("black").as_tuple()

                self.__matrix[i] = test_color.as_tuple()

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

            self.__matrix[num] = color.as_tuple()
            self.__matrix.write()

            time.sleep(delay)

            self.__matrix[num] = self.OFF
            self.__matrix.write()

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

    def __str__(self):
        return "NeoMatrix(pin=%d,px_count=%d/%d)" % (self.PIN, self.PIXELS, len(self.__matrix))

import time
from machine import RTC

from color_set import ColorSet

class Digit:
    TEMPLATE = [
        (0,0), (0,1), (0,2),
        (1,0),        (1,2),
        (2,0), (2,1), (2,2),
        (3,0),        (3,2),
        (4,0), (4,1), (4,2),
    ]

    ZERO = [
        1,1,1,
        1,  1,
        1,0,1,
        1,  1,
        1,1,1,
    ]

    ONE = [
        0,0,1,
        0,  1,
        0,0,1,
        0,  1,
        0,0,1,
    ]
    TWO = [
        1,1,1,
        0,  1,
        1,1,1,
        1,  0,
        1,1,1,
    ]
    THREE = [
        1,1,1,
        0,  1,
        1,1,1,
        0,  1,
        1,1,1,
    ]
    FOUR = [
        1,0,1,
        1,  1,
        1,1,1,
        0,  1,
        0,0,1,
    ]
    FIVE = [
        1,1,1,
        1,  0,
        1,1,1,
        0,  1,
        1,1,1,
    ]
    SIX = [
        1,0,0,
        1,  0,
        1,1,1,
        1,  1,
        1,1,1,
    ]
    SEVEN = [
        1,1,1,
        0,  1,
        0,0,1,
        0,  1,
        0,0,1,
    ]
    EIGHT = [
        1,1,1,
        1,  1,
        1,1,1,
        1,  1,
        1,1,1,
    ]
    NINE = [
        1,1,1,
        1,  1,
        1,1,1,
        0,  1,
        0,0,1,
    ]

    DIGITS = {
        0: ZERO,
        1: ONE,
        2: TWO,
        3: THREE,
        4: FOUR,
        5: FIVE,
        6: SIX,
        7: SEVEN,
        8: EIGHT,
        9: NINE
    }

    @classmethod
    def get_pixels(cls, digit):
        return cls.DIGITS[digit]

class DigitalClock:
    OFF          = ColorSet.BLACK
    # HOURS_COLORS = (ColorSet.CHRISTMAS[0], ColorSet.CHRISTMAS[1])
    HOURS_COLORS = (ColorSet.GREEN, ColorSet.BLUE)
    MINUTES_COLORS = (ColorSet.BLUE, ColorSet.GREEN)

    def __init__(self, matrix):
        self.__rtc = RTC()
        self.__matrix = matrix

    def __update(self):
        now = self.__rtc.datetime()
        hour = now[4]
        minutes = now[5]
        seconds = now[6]

        print("%02d:%02d:%02d" % (hour, minutes, seconds))

        if seconds % 10 == 0:
            self.__set_number(minutes, self.MINUTES_COLORS)
        else:
            self.__set_number(hour, self.HOURS_COLORS)

        # self.__set_number(seconds, self.HOURS_COLORS)

        self.__matrix.update()

    def __set_number(self, number, colors):
        # 1. split into digits
        d0 = int(number / 10)
        d1 = number % 10

        left_shift = 1
        for idx, digit in enumerate((d0, d1)):
            self.__draw_digit(digit, left_shift, colors[idx])
            left_shift += 3

    def __draw_digit(self, digit, offset, color):
        pixels = Digit.get_pixels(digit)
        for idx, loc in enumerate(Digit.TEMPLATE):
            if pixels[idx]:
                self.__matrix.set_rc(loc[0], loc[1]+offset, color)
            else:
                self.__matrix.set_rc(loc[0], loc[1]+offset, self.OFF)

    def test(self, limit=100):
        for i in range(0, limit):
            self.__set_number(i, self.HOURS_COLORS)
            self.__matrix.update()
            time.sleep(1)

    def tick(self):
        self.__update()

    def run(self):
        while True:
            self.tick()
            time.sleep(1)

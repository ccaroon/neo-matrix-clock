import time
from machine import RTC

from color_factory import ColorFactory

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
    COLOR_SET = ColorFactory.get_season("winter")

    OFF            = ColorFactory.get("black")
    HOURS_COLORS   = (COLOR_SET[0], COLOR_SET[1])
    MINUTES_COLORS = (COLOR_SET[1], COLOR_SET[0])
    SECONDS_COLOR  = COLOR_SET[2]
    AM_PM_COLOR    = COLOR_SET[2]

    AM_PIXELS = (
        (0,0), (1,0)
    )
    PM_PIXELS = (
        (3,0), (4,0)
    )

    SECONDS_PIXELS = (
        (4,7),
        # NOTE: something wrong with 3,7 #31?
        (4,7),
        (2,7),
        (1,7),
        (0,7)
    )

    def __init__(self, matrix, display24h = True):
        self.__rtc = RTC()
        self.__matrix = matrix
        self.__display24h = display24h


    def __update(self):
        now = self.__rtc.datetime()
        hour = now[4]
        minutes = now[5]
        seconds = now[6]
        is_am = True if hour < 12 else False

        print("%02d:%02d:%02d" % (hour, minutes, seconds))

        # Alternate showing hours & minutes every 10 seconds
        if int(seconds/5) % 2 == 0:
            if not self.__display24h:
                hour = hour-12 if hour > 12 else hour
            self.__set_number(hour, self.HOURS_COLORS, zero_pad=self.__display24h)
        else:
            self.__set_number(minutes, self.MINUTES_COLORS)

        # show AM/PM indicator
        # TODO: turn old off when changes to new
        am_pm_loc = self.AM_PIXELS if is_am else self.PM_PIXELS
        for loc in am_pm_loc:
            self.__matrix.set_rc(loc[0], loc[1], self.AM_PM_COLOR)

        # Seconds "blinker"
        count = int(seconds/12)
        for idx, loc in enumerate(self.SECONDS_PIXELS):
            color = self.SECONDS_COLOR if idx <= count else self.OFF
            # print("(%d,%d) = %s" % (loc[0], loc[1], color))
            self.__matrix.set_rc(loc[0], loc[1], color)

        self.__matrix.update()

    def __set_number(self, number, colors, zero_pad=True):
        # 1. split into digits
        d0 = int(number / 10)
        d1 = number % 10

        col_offset = 1
        for idx, digit in enumerate((d0, d1)):
            color = self.OFF if idx == 0 and digit == 0 and zero_pad is False else colors[idx]
            self.__draw_digit(digit, col_offset, color)
            col_offset += 3

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

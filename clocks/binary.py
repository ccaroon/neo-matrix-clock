import time
from machine import RTC

from color_factory import ColorFactory

class BinaryClock:

    OFF          = ColorFactory.get("black")
    SEASON       = ColorFactory.get_season("winter")
    HOUR_COLOR   = SEASON[0]
    MINUTE_COLOR = SEASON[1]
    SECOND_COLOR = SEASON[2]

    # As Row,Col tuples
    HOUR_PIXELS = [
        ( (1,1), (2,1), (3,1), (4,1) ),
        ( (1,2), (2,2), (3,2), (4,2) )
    ]

    # As Row,Col tuples
    MINUTE_PIXELS = [
        ( (1,3), (2,3), (3,3), (4,3) ),
        ( (1,4), (2,4), (3,4), (4,4) )
    ]

    # As Row,Col tuples
    SECOND_PIXELS = [
        ( (1,5), (2,5), (3,5), (4,5) ),
        ( (1,6), (2,6), (3,6), (4,6) )
    ]

    def __init__(self, matrix):
        self.__rtc = RTC()
        self.__matrix = matrix

    def __update(self):
        now = self.__rtc.datetime()
        hour = now[4]
        minutes = now[5]
        seconds = now[6]

        print("%02d:%02d:%02d" % (hour, minutes, seconds))
        self.__set_number(hour, self.HOUR_PIXELS, self.HOUR_COLOR)
        self.__set_number(minutes, self.MINUTE_PIXELS, self.MINUTE_COLOR)
        self.__set_number(seconds, self.SECOND_PIXELS, self.SECOND_COLOR)

        self.__matrix.update()

    def __set_number(self, number, pixel_set, on_color):
        # 1. split into digits
        d0 = int(number / 10)
        d1 = number % 10

        # 2. convert digit to binary string, zero-padded to 4 places
        d0_bin = "{:04b}".format(d0)
        d1_bin = "{:04b}".format(d1)

        # 3. display on matrix
        for digit, bin_str in enumerate((d0_bin, d1_bin)):
            for idx, bin_value in enumerate(bin_str):
                color = None
                if int(bin_value) == 0:
                    color = self.OFF
                else:
                    color = on_color

                self.__matrix.set_rc(
                    pixel_set[digit][idx][0],
                    pixel_set[digit][idx][1],
                    color
                )

    def tick(self):
        self.__update()

    def run(self):
        while True:
            self.tick()
            time.sleep(1)

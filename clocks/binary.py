import time
from machine import RTC

class BinaryClock:

    OFF = (0,0,0,0)
    HOUR_ON   = (128,0,0,0)
    SECOND_ON = (0,128,0,0)
    MINUTE_ON = (0,0,128,0)

    HOUR = [
        ( (1,1), (2,1), (3,1), (4,1) ),
        ( (1,2), (2,2), (3,2), (4,2) )
    ]

    MINUTES = [
        ( (1,3), (2,3), (3,3), (4,3) ),
        ( (1,4), (2,4), (3,4), (4,4) )
    ]

    SECONDS = [
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
        self.__set_number(hour, self.HOUR, self.HOUR_ON)
        self.__set_number(seconds, self.SECONDS, self.SECOND_ON)
        self.__set_number(minutes, self.MINUTES, self.MINUTE_ON)

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

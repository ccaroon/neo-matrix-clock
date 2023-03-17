import time
from machine import RTC
import random

from lib.colors.color_factory import ColorFactory
from lib.colors.season import Season
from lib.colors.holiday import Holiday

class Clock:
    UPDATE_FREQ = 1 # in seconds
    USE_RANDOM_COLOR_SET = False

    def __init__(self, matrix):
        self._rtc = RTC()
        self._matrix = matrix

        self.__last_update = 0

    def _tick(self, update_display=False):
        """ Called to 'tick' the Clock """
        raise NotImplementedError("Must be overridden in sub-class with code that `ticks' the Clock")

    def _get_hms(self):
        now = self._rtc.datetime()
        return (now[4], now[5], now[6])

    def _daily_random_color_set(self):
        now = self._rtc.datetime()
        random.seed(now[0]*10000 + now[1]*100 + now[2])

        color_set = ColorFactory.random(count=4)
        return color_set

    def _get_color_set(self):
        (hour, _, _) = self._get_hms()

        color_set = Holiday.get("current")
        if not color_set:
            if self.USE_RANDOM_COLOR_SET or hour % 2 == 0:
                color_set = self._daily_random_color_set()
            else:
                color_set = Season.get("current")

        return color_set

    def reset(self):
        self.__last_update = 0

    def tick(self):
        now = time.localtime()
        now_secs = time.mktime(now)

        update_display = now_secs - self.__last_update >= self.UPDATE_FREQ
        if update_display:
            print("%s - %02d:%02d:%02d" % (type(self).__name__, now[3], now[4], now[5]))
            self.__last_update = now_secs

        self._tick(update_display)
        self._matrix.update()

    def run(self):
        while True:
            self.tick()
            time.sleep(1)

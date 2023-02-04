import time
from machine import RTC

class Clock:
    UPDATE_FREQ = 1 # in seconds

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

import time
from machine import RTC

class Clock:
    # Time (in seconds) between ticks
    TICK_INTERVAL = 1

    def __init__(self, matrix):
        self._rtc = RTC()
        self._matrix = matrix

    def _update(self):
        """ Called to Update the Clock Display """
        raise NotImplementedError("Must be overridden in sub-class with code that updates the Clock display")

    def _get_hms(self):
        now = self._rtc.datetime()
        return (now[4], now[5], now[6])

    def tick(self):
        self._update()
        self._matrix.update()

    def run(self):
        while True:
            self.tick()
            time.sleep(1)

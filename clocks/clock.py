import time
from machine import RTC

class Clock:
    def __init__(self, matrix):
        self._rtc = RTC()
        self._matrix = matrix

    def _update():
        """ Called to Update the Clock Display """
        raise NotImplementedError("Must be overridden in sub-class with code that updates the Clock display")

    def tick(self):
        self._update()
        self._matrix.update()

    def run(self):
        while True:
            self.tick()
            time.sleep(1)

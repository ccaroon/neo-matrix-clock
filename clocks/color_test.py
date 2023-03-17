# import time
# from lib.colors.color_factory import ColorFactory
# from lib.glyph import Glyph

from lib.colors.holiday import Holiday
from lib.colors.season import Season

from .clock import Clock

class ColorTestClock(Clock):
    UPDATE_FREQ = 5 * 60
    # OFF = ColorFactory.get("black")

    def __init__(self, matrix):
        super().__init__(matrix)

    def _tick(self, update_display=False):
        if update_display:
            # colors = Season.get_current()
            colors = Holiday.get("st_patricks")

            self._matrix.fill_column(0, colors[0])
            self._matrix.fill_column(1, colors[0])

            self._matrix.fill_column(2, colors[1])
            self._matrix.fill_column(3, colors[1])

            self._matrix.fill_column(4, colors[2])
            self._matrix.fill_column(5, colors[2])

            self._matrix.fill_column(6, colors[3])
            self._matrix.fill_column(7, colors[3])

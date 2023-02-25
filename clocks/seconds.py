import time
from lib.colors.color_factory import ColorFactory
from lib.glyph import Glyph

from .clock import Clock

class SecondsClock(Clock):
    OFF = ColorFactory.get("black")

    def __init__(self, matrix):
        super().__init__(matrix)

    def _tick(self, update_display=False):
        (_, _, seconds) = self._get_hms()

        color_set = self._get_color_set()

        if seconds % 2 == 0:
            colors = (color_set[0], color_set[1])
        else:
            colors = (color_set[2], color_set[3])

        self._set_number(seconds, colors)

    def _set_number(self, number, colors, zero_pad=True):
        # 1. split into digits
        d0 = int(number / 10)
        d1 = number % 10

        col_offset = 1
        for idx, digit in enumerate((d0, d1)):
            color = self.OFF if idx == 0 and digit == 0 and zero_pad is False else colors[idx]
            glyph = Glyph.get(digit)
            self._matrix.draw_glyph(glyph, color, col_offset=col_offset)
            col_offset += 3

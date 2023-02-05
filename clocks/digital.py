import time
from lib.colors.color_factory import ColorFactory
from lib.glyph import Glyph

from .clock import Clock

class DigitalClock(Clock):
    OFF = ColorFactory.get("black")

    AM_PIXELS = (
        (0,0), (1,0)
    )
    PM_PIXELS = (
        (3,0), (4,0)
    )

    SECONDS_PIXELS = (
        (4,7),
        (3,7),
        (2,7),
        (1,7),
        (0,7)
    )

    def __init__(self, matrix, display24h = True):
        super().__init__(matrix)
        self.__display24h = display24h

    def __get_colors(self):
        color_set = self._get_color_set()

        colors = {
            "hours": (color_set[0], color_set[1]),
            "mins":  (color_set[1], color_set[0]),
            "secs":  color_set[3],
            "am_pm": color_set[2]
        }

        return colors

    def _tick(self, update_display=False):
        (hour, minutes, seconds) = self._get_hms()
        is_am = True if hour < 12 else False

        colors = self.__get_colors()

        # Alternate showing hours & minutes every 10 seconds
        if int(seconds/5) % 2 == 0:
            if not self.__display24h:
                hour = hour-12 if hour > 12 else hour
            self._set_number(hour, colors["hours"], zero_pad=self.__display24h)
        else:
            self._set_number(minutes, colors["mins"])

        # show AM/PM indicator
        am_pm_on = None
        am_pm_off = None
        if is_am:
            am_pm_on = self.AM_PIXELS
            am_pm_off = self.PM_PIXELS
        else:
            am_pm_on = self.PM_PIXELS
            am_pm_off = self.AM_PIXELS

        for loc in am_pm_on:
            self._matrix.set_rc(loc[0], loc[1], colors["am_pm"])

        for loc in am_pm_off:
            self._matrix.set_rc(loc[0], loc[1], self.OFF)

        # Seconds "ticker"
        count = seconds % 5
        count2min = int(seconds/12)
        for idx, loc in enumerate(self.SECONDS_PIXELS):
            if idx <= count:
                color = colors["secs"]
                if idx <= count2min:
                    color = colors["am_pm"]
                self._matrix.set_rc(loc[0], loc[1], color)
            else:
                self._matrix.set_rc(loc[0], loc[1], self.OFF)

    def test(self):
        color = ColorFactory.get("green")
        for i in range(10):
            glyph = Glyph.get(i)
            self._matrix.draw_glyph(glyph, color, col_offset=2)
            self._matrix.update()
            time.sleep(1)

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

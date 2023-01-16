from lib.colors.color_factory import ColorFactory
from lib.colors.season import Season
from lib.glyph import Glyph

from .clock import Clock

class DigitalClock(Clock):
    # COLOR_SET = ColorFactory.random(count=3)
    COLOR_SET = Season.get("current")
    # COLOR_SET = ColorFactory.random(count=3)
    # COLOR_SET = [
    #     ColorFactory.get("orange"),
    #     ColorFactory.get("blue"),
    #     ColorFactory.get("cyan", brightness=0.10)
    # ]

    OFF            = ColorFactory.get("black")
    HOURS_COLORS   = (COLOR_SET[0], COLOR_SET[1])
    MINUTES_COLORS = (COLOR_SET[1], COLOR_SET[0])
    SECONDS_COLOR  = COLOR_SET[3]
    AM_PM_COLOR    = COLOR_SET[2]

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

    def _update(self):
        (hour, minutes, seconds) = self._get_hms()
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
        am_pm_on = None
        am_pm_off = None
        if is_am:
            am_pm_on = self.AM_PIXELS
            am_pm_off = self.PM_PIXELS
        else:
            am_pm_on = self.PM_PIXELS
            am_pm_off = self.AM_PIXELS

        for loc in am_pm_on:
            self._matrix.set_rc(loc[0], loc[1], self.AM_PM_COLOR)

        for loc in am_pm_off:
            self._matrix.set_rc(loc[0], loc[1], self.OFF)

        # Seconds "ticker"
        count = seconds % 5
        count2min = int(seconds/12)
        for idx, loc in enumerate(self.SECONDS_PIXELS):
            if idx <= count:
                color = self.SECONDS_COLOR
                if idx <= count2min:
                    color = self.AM_PM_COLOR
                self._matrix.set_rc(loc[0], loc[1], color)
            else:
                self._matrix.set_rc(loc[0], loc[1], self.OFF)

    def __set_number(self, number, colors, zero_pad=True):
        # 1. split into digits
        d0 = int(number / 10)
        d1 = number % 10

        col_offset = 1
        for idx, digit in enumerate((d0, d1)):
            color = self.OFF if idx == 0 and digit == 0 and zero_pad is False else colors[idx]
            glyph = Glyph.get(digit)
            self._matrix.draw_glyph(glyph, color, col_offset=col_offset)
            col_offset += 3

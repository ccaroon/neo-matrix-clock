from machine import RTC

from lib.colors.color import Color
from lib.colors.color_factory import ColorFactory

class Holiday:
    __RTC = RTC()

    NEWYEAR = 101
    VALENTINES = 214
    BIRTHDAY = 219
    STPATTY = 317
    INDYPENDY = 704
    HALLOWEEN = 1031
    # Not *exactly* the correct day, but close enough :)
    THANKSGIVING = 1125
    CHRISTMAS = 1225
    TODAY = 108

    HOLIDAYS = {
        # For Testing Purposes
        "today": (
            ColorFactory.get("red"),
            ColorFactory.get("green"),
            ColorFactory.get("blue"),
            ColorFactory.get("white")
        ),
        "new_years": (
            ColorFactory.get("white"),  # white
            ColorFactory.get("yellow"), # yellow
            ColorFactory.hex("AF00FF"), # purple
            ColorFactory.hex("0096C8")  # blue
        ),
        "valentines": (
            ColorFactory.get("red"),    # red
            ColorFactory.get("white"),  # white
            ColorFactory.hex("FF4545"), # pink
            ColorFactory.get("black")   # off
        ),
        "birthday": (
        #     {red : 0, green : 255, blue : 0},   # green
        #     {red : 255, green : 0, blue : 255}, # purple
        #     {red : 0, green : 0, blue : 255},   # blue
        #     {red : 255, green : 255, blue : 0}, # yellow
        ),
        "st_patricks": (
        #     off,
        #     {red : 0, green : 255, blue : 0},     # green
        #     {red : 255, green : 255, blue : 255}, # white
        #     {red : 40, green : 255, blue : 40},   # light-green
        ),
        "independence": (
        #     off,
        #     {red : 255, green : 0, blue : 0},     # red
        #     {red : 255, green : 255, blue : 255}, # white
        #     {red : 0, green : 0, blue : 255},     # blue
        ),
        "halloween": (
        #     {red : 255, green : 255, blue : 255}, # white
        #     {red : 255, green : 100, blue : 0},   # orange
        #     {red : 255, green : 0, blue : 255},   # purple
        #     {red : 0, green : 255, blue : 0},     # green
        ),
        "thanksgiving": (
        #     {red : 255, green : 255, blue : 255}, # white
        #     {red : 255, green : 0, blue : 0},     # red
        #     {red : 240, green : 255, blue : 0},   # yellow
        #     {red : 255, green : 100, blue : 0},   # orange
        ),
        "christmas": (
        #     {red : 255, green : 255, blue : 255}, # white
        #     {red : 0, green : 255, blue : 0},     # green
        #     {red : 255, green : 0, blue : 0},     # red
        #     {red : 75, green : 150, blue : 255},  # light-blue
        ),
    }

    HOLIDAY_MAP = {
        NEWYEAR: "new_years",
        VALENTINES: "valentines",
        BIRTHDAY: "birthday",
        STPATTY: "st_patricks",
        INDYPENDY: "independence",
        HALLOWEEN: "halloween",
        THANKSGIVING: "thanksgiving",
        CHRISTMAS: "christmas",
        TODAY: "today"
    }

    @classmethod
    def get(cls, name, brightness=Color.DEFAULT_BRIGHTNESS):
        if name == "current":
            colors = cls.get_current(brightness)
        else:
            colors = cls.HOLIDAYS.get(name)

        if colors is None:
            raise ValueError("Unknown Holiday: '%d'" % name)

        for color in colors:
            color.brightness = brightness

        return colors

    @classmethod
    def get_current(cls, brightness=Color.DEFAULT_BRIGHTNESS):
        # date == year, month, day, weekday, hour, minute, second, microsecond
        now = cls.__RTC.datetime()
        month = now[1]
        day = now[2]
        date_code = (month * 100) + day
        color_set = None

        name = cls.HOLIDAY_MAP.get(date_code, None)
        if name is not None:
            color_set = cls.get(name, brightness)

        return color_set

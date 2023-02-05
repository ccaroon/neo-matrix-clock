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
            ColorFactory.get("white"),
            ColorFactory.get("yellow"),
            ColorFactory.hex("AF00FF"), # purple
            ColorFactory.hex("0096C8")  # blue
        ),
        "valentines": (
            ColorFactory.get("red"),
            ColorFactory.get("white"),
            ColorFactory.hex("FF4545"), # pink
            ColorFactory.get("black")
        ),
        "birthday": (
            ColorFactory.get("green"),
            ColorFactory.get("violet"),
            ColorFactory.get("yellow"),
            ColorFactory.get("blue")
        ),
        "st_patricks": (
            ColorFactory.get("green"),
            ColorFactory.get("white"),
            ColorFactory.hex("28FF28"), # light-green
            ColorFactory.get("black")
        ),
        "independence": (
            ColorFactory.get("red"),
            ColorFactory.get("white"),
            ColorFactory.get("blue"),
            ColorFactory.get("black")
        ),
        "halloween": (
            ColorFactory.get("orange"),
            ColorFactory.get("violet"),
            ColorFactory.get("green"),
            ColorFactory.get("white")
        ),
        "thanksgiving": (
            ColorFactory.get("red"),
            ColorFactory.get("yellow"),
            ColorFactory.get("orange"),
            ColorFactory.get("white")
        ),
        "christmas": (
            ColorFactory.get("white"),
            ColorFactory.get("green"),
            ColorFactory.get("red"),
            ColorFactory.hex("4B96FF")  # light-blue
        ),
    }

    HOLIDAY_MAP = {
        TODAY: "today",
        NEWYEAR: "new_years",
        VALENTINES: "valentines",
        BIRTHDAY: "birthday",
        STPATTY: "st_patricks",
        INDYPENDY: "independence",
        HALLOWEEN: "halloween",
        THANKSGIVING: "thanksgiving",
        CHRISTMAS: "christmas"
    }

    @classmethod
    def get(cls, name, brightness=Color.DEFAULT_BRIGHTNESS):
        if name == "current":
            colors = cls.get_current(brightness)
        else:
            colors = cls.HOLIDAYS.get(name)
            if colors is None:
                raise ValueError("Unknown Holiday: '%s'" % name)

        if colors is not None:
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

import random
from lib.colors.color import Color

class ColorFactory:
    COLORS = {
        # b&w
        "black": Color(0,0,0),
        "white": Color(255,255,255),
        "white_rgbw": Color(0,0,0,255),

        # rainbow
        "red": Color(255,0,0),
        "orange": Color(255,128,0),
        "yellow": Color(255,255,0),
        "green": Color(0,255,0),
        "blue": Color(0,0,255),
        "indigo": Color(75,0,255),
        "violet": Color(128,0,255),

        # other
        "cyan": Color(0,255,128),
        "purple": Color(255,0,255),
        "pink": Color(255,1,80)
    }

    HOLIDAYS = {
        "christmas": (
            COLORS["white"],
            COLORS["green"],
            COLORS["red"],
            Color(75, 150, 255) # light-blue'ish
        )
    }

    @classmethod
    def get(cls, name, brightness=Color.DEFAULT_BRIGHTNESS):
        color = cls.COLORS.get(name)
        if color is None:
            raise ValueError("Unknown Color: '%d'" % name)

        color.brightness = brightness
        return color

    @classmethod
    def random(cls, count=1, brightness=Color.DEFAULT_BRIGHTNESS):
        color_set = []
        for _ in range(count):
            red = random.randint(0,255)
            green = random.randint(0,255)
            blue = random.randint(0,255)

            color_set.append(Color(red, green, blue))

        return color_set[0] if len(color_set) == 1 else color_set

    @classmethod
    def hex(self, hex_str):
        red = int(hex_str[0:2], 16)
        green = int(hex_str[2:4], 16)
        blue= int(hex_str[4:6], 16)

        return Color(red, green, blue)

    @classmethod
    def __get_color_set(cls, color_set, name, brightness):
        colors = color_set.get(name)

        if colors is None:
            raise ValueError("Unknown Color Set: '%d'" % name)

        for color in colors:
            color.brightness = brightness

        return colors

    @classmethod
    def get_holiday(cls, name, brightness=Color.DEFAULT_BRIGHTNESS):
        return cls.__get_color_set(cls.HOLIDAYS, name, brightness)
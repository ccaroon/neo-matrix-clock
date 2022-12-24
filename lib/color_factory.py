from color import Color

class ColorFactory:

    COLORS = {
        "black": Color(0,0,0),
        "white": Color(255,255,255,0),
        "red": Color(255,0,0),
        "orange": Color(255,255,0),
        "yellow": Color(255,255,0),
        "green": Color(0,255,0),
        "blue": Color(0,0,255),
        "indigo": Color(75,0,255),
        "violet": Color(128,0,255),
        "cyan": Color(0,255,128)
    }

    SEASONS = {
        "winter": (
            Color(0, 128, 255), # blue'ish
            COLORS["cyan"],
            COLORS["white"]
        )
    }

    HOLIDAYS = {
        "christmas": (
            COLORS["violet"],
            COLORS["green"],
            COLORS["red"],
            Color(75, 150, 255) # light-blue'ish
        )
    }

    @classmethod
    def get(cls, name, brightness=0.50):
        color = cls.COLORS.get(name)
        if color is None:
            raise ValueError("Unknown Color: '%d'" % name)

        color.brightness = brightness
        return color

    @classmethod
    def __get_color_set(cls, color_set, name, brightness):
        colors = color_set.get(name)

        if colors is None:
            raise ValueError("Unknown Color Set: '%d'" % name)

        for color in colors:
            color.brightness = brightness

        return colors

    @classmethod
    def get_season(cls, name, brightness=0.50):
        return cls.__get_color_set(cls.SEASONS, name, brightness)

    @classmethod
    def get_holiday(cls, name, brightness=0.50):
        return cls.__get_color_set(cls.HOLIDAYS, name, brightness)

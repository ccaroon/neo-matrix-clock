from lib.colors.color import Color
from lib.colors.color_factory import ColorFactory

class Temperature:
    FREEZING    = { "range": range(0,26),   "color": ColorFactory.hex("0xffffff") }
    REALLY_COLD = { "range": range(26,33),  "color": ColorFactory.hex("0x2222ff") }
    COLD        = { "range": range(33,56),  "color": ColorFactory.hex("0x0077ff") }
    COOL        = { "range": range(56,65),  "color": ColorFactory.hex("0x04fbe8") }
    COMFORTABLE = { "range": range(65,76),  "color": ColorFactory.hex("0x33e108") }
    WARM        = { "range": range(76,86),  "color": ColorFactory.hex("0xf9f504") }
    HOT         = { "range": range(86,96),  "color": ColorFactory.hex("0xf97304") }
    REALLY_HOT  = { "range": range(96,200), "color": ColorFactory.hex("0xff0000") }

    TEMP_RANGES = (
        FREEZING,
        REALLY_COLD,
        COLD,
        COOL,
        COMFORTABLE,
        WARM,
        HOT,
        REALLY_HOT
    )

    TEMPS = {
        "freezing": (
            ColorFactory.hex("0x11111111"),
            FREEZING["color"],
            REALLY_COLD["color"],
            COLD["color"]
        ),
        "really_cold": (
            FREEZING["color"],
            REALLY_COLD["color"],
            COLD["color"],
            COOL["color"]
        ),
        "cold": (
            REALLY_COLD["color"],
            COLD["color"],
            COOL["color"],
            COMFORTABLE["color"]
        ),
        "cool": (
            COLD["color"],
            COOL["color"],
            COMFORTABLE["color"],
            WARM["color"]
        ),
        "comfortable": (
            COOL["color"],
            COMFORTABLE["color"],
            WARM["color"],
            HOT["color"]
        ),
        "warm": (
            COMFORTABLE["color"],
            WARM["color"],
            HOT["color"],
            REALLY_HOT["color"]
        ),
        "hot": (
            WARM["color"],
            HOT["color"],
            REALLY_HOT["color"],
            REALLY_HOT["color"],
        ),
        "really_hot": (
            HOT["color"],
            REALLY_HOT["color"],
            REALLY_HOT["color"],
            REALLY_HOT["color"],
        )
    }


    @classmethod
    def from_temp(cls, temp):
        color = ColorFactory.hex("0xFFFFFF")

        for temp_range in cls.TEMP_RANGES:
            if temp in temp_range["range"]:
                color = temp_range["color"]
                break

        return color

    @classmethod
    def get(cls, name, brightness=Color.DEFAULT_BRIGHTNESS):
        if name == "current":
            colors = cls.get_current(brightness)
        else:
            colors = cls.TEMPS.get(name)

        if colors is None:
            raise ValueError("Unknown Temperature Range: '%d'" % name)

        for color in colors:
            color.brightness = brightness

        return colors

    @classmethod
    def get_current(cls, brightness=Color.DEFAULT_BRIGHTNESS):
        color_set = None
        # TODO
        return color_set

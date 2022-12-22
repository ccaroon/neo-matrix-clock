from color import Color

class ColorSet:
    BLACK  = Color(0,0,0)
    WHITE  = Color(0,0,0,64)

    RED    = Color(128,0,0)
    ORANGE = Color(128,64,0)
    YELLOW = Color(128,128,0)
    GREEN  = Color(0,128,0)
    BLUE   = Color(0,0,128)
    INDIGO = Color(75,0,255)
    VIOLET = Color(128,0,255)

    WINTER = (
        Color(0, 64, 128), # blue'ish
        Color(0, 128, 64), # cyan
        WHITE              # white
    )

    CHRISTMAS = (
        WHITE,
        GREEN,
        RED,
        Color(75, 150, 255) # light-blue'ish
    )

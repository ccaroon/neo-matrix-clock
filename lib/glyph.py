from lib.glyphs import get_digit
# from lib.glyphs.alpha import get_alpha

class Glyph:
    # data == [{"row", "col", "color"}]
    def __init__(self, data):
        self.__data = data

    def __iter__(self):
        return iter(self.__data)

    @classmethod
    def get(cls, char):
        glyph = None
        alpha_num = str(char)

        ascii = ord(alpha_num)
        if ascii in range(ord("0"), ord("9")+1):
            glyph_data = get_digit(alpha_num)
            glyph = Glyph(glyph_data)

        return glyph

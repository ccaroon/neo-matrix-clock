import lib.glyphs.digit as digit
import lib.glyphs.emoji as emoji

class Glyph:
    # data == [{"row", "col", "color"}]
    def __init__(self, data):
        self.__data = data

    def __iter__(self):
        return iter(self.__data)

    @classmethod
    def get(cls, name):
        glyph_data = cls.__get_data(name)
        glyph = Glyph(glyph_data)

        return glyph

    @classmethod
    def __get_data(cls, name):
        data = []
        pixels = None
        template = None

        # TODO: better way to decide glyph set
        glyph_name = str(name)
        if glyph_name in digit.DATA.keys():
            template = digit.TEMPLATE
            pixels = digit.DATA.get(glyph_name)
        elif glyph_name in emoji.DATA.keys():
            template = emoji.TEMPLATE
            pixels = emoji.DATA.get(glyph_name)

        # TODO: error handling if glyph set not found

        for idx, loc in enumerate(template):
            px_data = {
                "row": loc[0],
                "col": loc[1],
                "on": False
            }
            if pixels[idx] == 1:
                px_data["on"] = True

            data.append(px_data)

        return data

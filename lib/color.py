class Color:

    DEFAULT_BRIGHTNESS = 0.25

    def __init__(self, red, green, blue, white=0, **kwargs):
        # number between 0.0 & 1.0
        # E.g. .5 = 50% | .25 = 25%
        self.brightness = kwargs.get('brightness', self.DEFAULT_BRIGHTNESS)

        self.__red = red
        self.__green = green
        self.__blue = blue
        self.__white = white

    def as_tuple(self):
        return (
            int(self.__red   * self.brightness),
            int(self.__green * self.brightness),
            int(self.__blue  * self.brightness),
            int(self.__white * self.brightness)
        )

    def __str__(self) -> str:
        return str(self.as_tuple())

class Color:
    def __init__(self, red, green, blue, white=0):
        self.__red = red
        self.__green = green
        self.__blue = blue
        self.__white = white

    def as_tuple(self):
        return (self.__red, self.__green, self.__blue, self.__white)

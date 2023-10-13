from .digital import DigitalClock

from lib.weather_station import WeatherStation
from lib.colors.color_factory import ColorFactory
from lib.colors.temperature import Temperature
from lib.glyph import Glyph

class WeatherClock(DigitalClock):
    OFF = ColorFactory.get("black")
    ERROR_COLOR = ColorFactory.get("red")

    # In seconds
    UPDATE_FREQ = 5 * 60

    HUMIDITY_PIXELS = (
        (4,0),
        (3,0),
        (2,0),
        (1,0),
        (0,0)
    )

    def __init__(self, matrix, display24h = True):
        super().__init__(matrix, display24h)
        self.__weather_station = WeatherStation()

    def __humd_to_color(self, humd):
        color = None

        if humd <= 25:
            color = ColorFactory.hex("0xFFFFFF")
        elif humd > 25 and humd <= 50:
            color = ColorFactory.hex("0x8080FF")
        elif humd > 50 and humd <= 75:
            color = ColorFactory.hex("0x4040FF")
        else:
            color = ColorFactory.hex("0x2020FF")

        return color

    def __display_error(self, msg):
        print(msg)
        self._matrix.clear()
        glyph = Glyph.get("no")
        self._matrix.draw_glyph(glyph, self.ERROR_COLOR, col_offset=2)
        self._matrix.update()

    def __display_temperature(self):
        temp = self.__weather_station.temperature
        if temp:
            color_set = None
            if temp.age >= 10 * 60:
                color_set = [self.ERROR_COLOR, self.ERROR_COLOR]
            else:
                color = Temperature.from_temp(temp.value)
                color_set = [color, color]

            # can't display > 99
            display_temp = temp.value - 100 if temp.value >= 100 else temp.value
            self._set_number(display_temp, color_set)
        else:
            self.__display_error("Failed to get Temperature from WeatherStation feed.")

    def __display_humidity(self):
        humd = self.__weather_station.humidity
        if humd:
            color = self.__humd_to_color(humd.value)

            count = round(humd.value / 20)
            for idx, loc in enumerate(self.HUMIDITY_PIXELS):
                if idx < count:
                    self._matrix.set_rc(loc[0], loc[1], color)
                else:
                    self._matrix.set_rc(loc[0], loc[1], self.OFF)
        else:
            self.__display_error("Failed to get Humidity from WeatherStation feed.")

    def _tick(self, update_display=False):
        if update_display:
            self.__weather_station.sample()
            temp = self.__weather_station.temperature
            humd = self.__weather_station.humidity

            self.__display_temperature()
            self.__display_humidity()
            print("%d℉ | %d%%" % (temp.value, humd.value))
        else:
            temp = self.__weather_station.temperature
            (_, _, seconds) = self._get_hms()
            color = Temperature.from_temp(temp.value) if seconds % 2 == 0 else self.OFF
            self._matrix.set_rc(0,7, color)

    def test(self):
        for idx,humd in enumerate((5,35,65,95)):
            color = self.__humd_to_color(humd)
            self._matrix.set(idx, color)

        self._matrix.update()

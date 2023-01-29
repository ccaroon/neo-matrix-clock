import re
import time

from .digital import DigitalClock

from lib.adafruit_io import AdafruitIO
from lib.colors.color_factory import ColorFactory
from lib.glyph import Glyph
from lib.secrets import secrets

class WeatherClock(DigitalClock):

    OFF = ColorFactory.get("black")
    ERROR_COLOR = ColorFactory.get("red")

    # In minutes
    UPDATE_FREQ = 5

    HUMIDITY_PIXELS = (
        (4,0),
        (3,0),
        (2,0),
        (1,0),
        (0,0)
    )

    def __init__(self, matrix, display24h = True):
        super().__init__(matrix, display24h)

        self.__aio = AdafruitIO("weather-station")
        self.__temp = 0
        self.__humd = 0

        self.prep()

    def __temp_to_color(self, temp):
        color = ColorFactory.hex("FFFFFF")

        if temp <= 25:
            # white
            color = ColorFactory.hex("ffffff")
        elif temp > 25 and temp <= 32:
            # bluish/white
            color = ColorFactory.hex("e4f0fb")
        elif temp > 32 and temp <= 55:
            # blue
            color = ColorFactory.hex("047ffb")
        elif temp > 55 and temp <= 64:
            # cyan
            color = ColorFactory.hex("04fbe8")
        elif temp > 64 and temp <=75:
            # green
            color = ColorFactory.hex("33e108")
        elif temp > 75 and temp <= 85:
            # yellow
            color = ColorFactory.hex("f9f504")
        elif temp > 85 and temp <= 90:
            # orange
            color = ColorFactory.hex("f97304")
        else:
            # red
            color = ColorFactory.hex("ff0000")

        return color

    def __humd_to_color(self, humd):
        color = ColorFactory.hex("FFFFFF")

        if humd <= 25:
            color = ColorFactory.hex("FFFFFF")
        elif humd > 25 and humd <= 50:
            color = ColorFactory.hex("9999BB")
        elif humd > 50 and humd <= 75:
            color = ColorFactory.hex("9999DD")
        else:
            color = ColorFactory.hex("9999FF")

        return color


    def __display_error(self, msg):
        print(msg)
        self._matrix.clear()
        glyph = Glyph.get("no")
        self._matrix.draw_glyph(glyph, self.ERROR_COLOR, col_offset=2)
        self._matrix.update()

    # TODO: move this to Chronos?
    def __time_diff2now(self, date_str):
        # 2023-01-28T20:45:31Z - UTC
        match = re.match("(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)Z", date_str)
        time_t = (
            int(match.group(1)), int(match.group(2)), int(match.group(3)),
            int(match.group(4)), int(match.group(5)), int(match.group(6)),
            0, 0
        )
        # in UTC
        time_e = time.mktime(time_t)
        # Adjust for timezone
        # X hours in seconds
        time_e += secrets["tz_offset"] * (60 * 60)

        now = time.mktime(time.localtime())

        # For debuggin'
        # last = time.localtime(time_e)
        # curr = time.localtime()
        # print("last: %02d:%02d:%02d | now: %02d:%02d:%02d" % (
        #     last[3], last[4], last[5],
        #     curr[3], curr[4], curr[5]
        # ))
        # print("%s | %d | %d" % (date_str, now, time_e))

        return now - time_e

    def __display_temperature(self):
        print("...Sampling Temperature Data...")

        resp = self.__aio.get_data("temperature", fields=['created_at'])
        if resp['success']:
            self.__temp = int(resp["results"][0]["value"])

            # created_at is UTC
            # in seconds
            data_age = self.__time_diff2now(resp["results"][0]["created_at"])
            # print(data_age)

            if data_age >= 10 * 60:
                color = self.ERROR_COLOR
            else:
                color = self.__temp_to_color(self.__temp)

            # can't display > 99
            display_temp = self.__temp - 100 if self.__temp >= 100 else self.__temp
            self._set_number(display_temp, [color, color])
        else:
            self.__display_error("Failed to get Temperature from WeatherStation feed.")

    def __display_humidity(self):
        print("...Sampling Humidity Data...")

        resp = self.__aio.get_data("humidity")
        if resp['success']:
            self.__humd = int(resp["results"][0]["value"])
            count = round(self.__humd / 20)
            for idx, loc in enumerate(self.HUMIDITY_PIXELS):
                if idx < count:
                    color = self.__humd_to_color(self.__humd)
                    self._matrix.set_rc(loc[0], loc[1], color)
                else:
                    self._matrix.set_rc(loc[0], loc[1], self.OFF)
        else:
            self.__display_error("Failed to get Humidity from WeatherStation feed.")

    def _update(self):
        (_, minutes, seconds) = self._get_hms()

        if minutes % self.UPDATE_FREQ == 0 and seconds == 0:
            self.__display_temperature()
            self.__display_humidity()
        else:
            color = self.__temp_to_color(self.__temp) if seconds % 2 == 0 else self.OFF
            self._matrix.set_rc(0,7, color)
            print("(%02d:%02d) - %d℉ | %d%%" % (minutes, seconds, self.__temp, self.__humd))

    def prep(self):
        self.__display_temperature()
        self.__display_humidity()

    def test(self):
        temp = self.__aio.get_data("temperature")
        print(temp)
        self.__display_error("...Test...")

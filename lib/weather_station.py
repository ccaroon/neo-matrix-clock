import re
import time

from lib.adafruit_io import AdafruitIO
from lib.chronos import Chronos
from lib.config import Config

# -----------------------------------------------------------------------------
class Reading:
    name = None
    value = None
    age = None
    def __init__(self, name, value, age):
        self.name = name
        self.value = value
        self.age = age

    def __repr__(self):
        return (self.name, self.value, self.age)

    def __str__(self):
        return "%s: %d (%d sec)" % (self.name, self.value, self.age)

# -----------------------------------------------------------------------------
class WeatherStation:
    def __init__(self):
        self.__aio = AdafruitIO("weather-station")
        self.__temp = None
        self.__humd = None

    @property
    def humidity(self):
        return self.__humd

    @property
    def temperature(self):
        return self.__temp

    # TODO: move this to Chronos?
    def __time_diff2now(self, date_str):
        # 2023-01-28T20:45:31Z - UTC
        match = re.match("(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)Z", date_str)
        time_t = (
            int(match.group(1)), int(match.group(2)), int(match.group(3)),
            int(match.group(4)), int(match.group(5)), int(match.group(6)),
            0, 0
        )

        # UTC in seconds
        time_e = time.mktime(time_t)

        # Adjust for timezone & DST
        offset = Config.setting("datetime:tz_offset")
        if Chronos.is_dst():
            offset += 1

        # offset hours in seconds
        time_e +=  offset * (60 * 60)

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

    def display(self):
        print(self.__temp)
        print(self.__humd)

    def sample(self):
        self.__sample_temperature()
        self.__sample_humidity()

    def __sample_humidity(self):
        print("...Sampling Humidity Data...")

        resp = self.__aio.get_data("humidity", fields=['created_at'])
        if resp['success']:
            humd = int(resp["results"][0]["value"])
            data_age = self.__time_diff2now(resp["results"][0]["created_at"])
            self.__humd = Reading("humidity", humd, data_age)
        else:
            self.__humd = None

    def __sample_temperature(self):
        print("...Sampling Temperature Data...")

        resp = self.__aio.get_data("temperature", fields=['created_at'])
        if resp['success']:
            temp = int(resp["results"][0]["value"])
            data_age = self.__time_diff2now(resp["results"][0]["created_at"])
            self.__temp = Reading("temperature", temp, data_age)
        else:
            self.__temp = None

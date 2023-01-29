from chronos import Chronos
from secrets import secrets
from wifi import MyWifi

MyWifi.autoconnect()
Chronos.sync(tz_offset=secrets["tz_offset"])

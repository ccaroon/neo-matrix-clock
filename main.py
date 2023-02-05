# -- DEBUGGING
from lib.colors.color_factory import ColorFactory

# ------------------------------------------------------------------------------

# -- BUTTON TEST CODE --
# from machine import Pin
# button = Pin(27, Pin.IN, Pin.PULL_UP)
# button.irq(lambda p: print("Hello, World!") if p.value() == 1 else 0)
# ------------------------------------------------------------------------------

# -- SWITCHABLE CLOCKS
import time
from machine import Pin

from neo_matrix import NeoMatrix
from clocks.binary import BinaryClock
from clocks.digital import DigitalClock
from clocks.fibonacci import FibonacciClock
from clocks.weather import WeatherClock

button = Pin(27, Pin.IN, Pin.PULL_UP)

matrix = NeoMatrix(rgbw=False)
binary_clock = BinaryClock(matrix)
digital_clock = DigitalClock(matrix, display24h=False)
fib_clock = FibonacciClock(matrix)
weather_clock = WeatherClock(matrix, display24h=False)

CLOCKS = [
    binary_clock,
    digital_clock,
    weather_clock,
    fib_clock
]
CURRENT_CLOCK = 0

DEBOUNCE_DELAY = 75 # ms
DEBOUNCE_LAST = 0

def change_clock(p):
    global CLOCKS, CURRENT_CLOCK, DEBOUNCE_DELAY, DEBOUNCE_LAST

    if time.ticks_diff(time.ticks_ms(), DEBOUNCE_LAST) > DEBOUNCE_DELAY:
        DEBOUNCE_LAST = time.ticks_ms()
        if p.value() == 1:
            matrix.clear()
            CURRENT_CLOCK = 0 if CURRENT_CLOCK >= len(CLOCKS)-1 else CURRENT_CLOCK + 1
            CLOCKS[CURRENT_CLOCK].reset()

button.irq(change_clock)
while True:
    clock = CLOCKS[CURRENT_CLOCK]
    clock.tick()
    time.sleep(1)
# ------------------------------------------------------------------------------

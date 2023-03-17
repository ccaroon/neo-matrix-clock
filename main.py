# -- DEBUGGING
from lib.colors.color_factory import ColorFactory
from lib.glyph import Glyph
# ------------------------------------------------------------------------------


# For Testing Glyphs
def draw_glyph(i_name, c1, c2="black"):
    icon = Glyph.get(i_name)
    color1 = ColorFactory.get(c1)
    color2 = ColorFactory.get(c2)

    matrix.draw_glyph(icon, color1, color2=color2)
    matrix.update()

# -- BUTTON TEST CODE --
# from machine import Pin
# button = Pin(27, Pin.IN, Pin.PULL_UP)
# button.irq(lambda p: print("Hello, World!") if p.value() == 1 else 0)
# ------------------------------------------------------------------------------

# -- SWITCHABLE CLOCKS
import time
from machine import Pin, Timer

from neo_matrix import NeoMatrix
from clocks.binary import BinaryClock
# from clocks.color_test import ColorTestClock
from clocks.digital import DigitalClock
from clocks.fibonacci import FibonacciClock
# from clocks.seconds import SecondsClock
from clocks.weather import WeatherClock

button = Pin(27, Pin.IN, Pin.PULL_UP)
timer = Timer(0)

matrix = NeoMatrix(rgbw=False)
binary_clock = BinaryClock(matrix)
# color_clock = ColorTestClock(matrix)
digital_clock = DigitalClock(matrix, display24h=False)
fib_clock = FibonacciClock(matrix)
# sec_clock = SecondsClock(matrix)
weather_clock = WeatherClock(matrix, display24h=False)

CLOCKS = [
    # sec_clock,
    # color_clock,
    binary_clock,
    digital_clock,
    weather_clock,
    fib_clock
]
CURRENT_CLOCK = 0

DEBOUNCE_DELAY = 75 # ms
DEBOUNCE_LAST = 0

def change_clock():
    global CLOCKS, CURRENT_CLOCK

    matrix.clear()
    CURRENT_CLOCK = 0 if CURRENT_CLOCK >= len(CLOCKS)-1 else CURRENT_CLOCK + 1
    CLOCKS[CURRENT_CLOCK].reset()

def handle_timer(t):
    change_clock()

def handle_button(p):
    global DEBOUNCE_DELAY, DEBOUNCE_LAST

    if time.ticks_diff(time.ticks_ms(), DEBOUNCE_LAST) > DEBOUNCE_DELAY:
        DEBOUNCE_LAST = time.ticks_ms()
        if p.value() == 1:
            change_clock()

# Change the Clock when the button is pressed
button.irq(handle_button)

# Change the Clock every X seconds
PERIOD=6*60
timer.init(period=PERIOD*1000, callback=handle_timer)
# ------------------------------------------------------------------------------
while True:
    clock = CLOCKS[CURRENT_CLOCK]
    clock.tick()
    time.sleep(1)
# ------------------------------------------------------------------------------

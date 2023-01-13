# -- DEBUGGING
from lib.colors.color_factory import ColorFactory
# ------------------------------------------------------------------------------

# -- BINARY CLOCK --
# from neo_matrix import NeoMatrix
# from clocks.binary import BinaryClock

# matrix = NeoMatrix(rgbw=True)
# clock = BinaryClock(matrix)
# clock.run()
# ------------------------------------------------------------------------------

# -- DIGITAL CLOCK --
# from neo_matrix import NeoMatrix
# from clocks.digital import DigitalClock

# matrix = NeoMatrix(rgbw=True)
# clock = DigitalClock(matrix, display24h=False)
# clock.run()
# ------------------------------------------------------------------------------

# -- BUTTON TEST CODE --
# from machine import Pin

# button = Pin(27, Pin.IN, Pin.PULL_UP)
# button.irq(lambda p: print("Hello, World!") if p.value() == 1 else 0)
# ------------------------------------------------------------------------------

# -- SWITCHABLE
import time
from machine import Pin

from neo_matrix import NeoMatrix
from clocks.binary import BinaryClock
from clocks.digital import DigitalClock
from clocks.fibonacci import FibonacciClock

button = Pin(27, Pin.IN, Pin.PULL_UP)

matrix = NeoMatrix(rgbw=False)
binary_clock = BinaryClock(matrix)
digital_clock = DigitalClock(matrix, display24h=False)
fib_clock = FibonacciClock(matrix)

CLOCKS = [
    binary_clock,
    digital_clock,
    fib_clock
]
CURRENT_CLOCK = 0

def change_clock(p):
    global CLOCKS, CURRENT_CLOCK
    if p.value() == 1:
        matrix.clear()
        CURRENT_CLOCK = 0 if CURRENT_CLOCK >= len(CLOCKS)-1 else CURRENT_CLOCK + 1

button.irq(change_clock)
while True:
    clock = CLOCKS[CURRENT_CLOCK]
    clock.tick()
    time.sleep(clock.TICK_INTERVAL)
# ------------------------------------------------------------------------------

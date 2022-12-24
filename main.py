from neo_matrix import NeoMatrix
# from clocks.binary import BinaryClock
from clocks.digital import DigitalClock

matrix = NeoMatrix()

# Binary Clock
# clock = BinaryClock(matrix)

# Digital Clock
clock = DigitalClock(matrix, display24h=False)

clock.run()

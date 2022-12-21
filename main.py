from neo_matrix import NeoMatrix
from clocks.binary import BinaryClock

matrix = NeoMatrix()
clock = BinaryClock(matrix)
clock.run()

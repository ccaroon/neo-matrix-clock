import random

from lib.colors.color_factory import ColorFactory

from .clock import Clock
class FibonacciClock(Clock):

    UPDATE_FREQ = 60 # seconds

    OFF        = None
    ONE        = "one"
    ONE_PRIME  = "one-prime"
    TWO        = "two"
    THREE      = "three"
    FIVE       = "five"

    BOXES = {
        ONE: (
            (1,2),
        ),
        ONE_PRIME: (
            (0,2),
        ),
        TWO: (
            (0,0), (0,1),
            (1,0), (1,1)
        ),
        THREE: (
            (2,0), (2,1), (2,2),
            (3,0), (3,1), (3,2),
            (4,0), (4,1), (4,2)
        ),
        FIVE: (
            (0,3), (0,4), (0,5), (0,6), (0,7),
            (1,3), (1,4), (1,5), (1,6), (1,7),
            (2,3), (2,4), (2,5), (2,6), (2,7),
            (3,3), (3,4), (3,5), (3,6), (3,7),
            (4,3), (4,4), (4,5), (4,6), (4,7)
        )
    }

    NUMBER_MAP = (
        # ZERO => All lights off
        (
            (OFF, OFF, OFF, OFF, OFF),
        ),

        # ONE =>  1 | 1`
        (
            (ONE,       OFF, OFF, OFF, OFF),
            (ONE_PRIME, OFF, OFF, OFF, OFF),
        ),

        # TWO => 1,1` | 2
        (
            (ONE, ONE_PRIME, OFF, OFF, OFF),
            (TWO, OFF, OFF, OFF, OFF),
        ),

        # THREE => 1,2 | 1`,2 | 3
        (
            (ONE, TWO, OFF, OFF, OFF),
            (ONE_PRIME, TWO, OFF, OFF, OFF),
            (THREE, OFF, OFF, OFF, OFF),
        ),

        # FOUR => 1,3 | 1`,3 | 1,1`,2
        (
            (ONE, THREE, OFF, OFF, OFF),
            (ONE_PRIME, THREE, OFF, OFF, OFF),
            (ONE, ONE_PRIME, TWO, OFF, OFF),
        ),

        # FIVE => 1,1`,3 | 2,3 | 5
        (
            (ONE, ONE_PRIME, THREE, OFF, OFF),
            (TWO, THREE, OFF, OFF, OFF),
            (FIVE, OFF, OFF, OFF, OFF),
        ),

        # SIX =>  1,5 | 1`,5 | 1,2,3 | 1`,2,3
        (
            (ONE, FIVE, OFF, OFF, OFF),
            (ONE_PRIME, FIVE, OFF, OFF, OFF),
            (ONE, TWO, THREE, OFF, OFF),
            (ONE_PRIME, TWO, THREE, OFF, OFF),
        ),

        # SEVEN => 2,5 | 1,1`,2,3
        (
            (TWO, FIVE,      OFF, OFF,   OFF),
            (ONE, ONE_PRIME, TWO, THREE, OFF),
        ),

        # EIGHT => 3,5 | 1,2,5 | 1`,2,5
        (
            (THREE, FIVE, OFF, OFF, OFF),
            (ONE, TWO, FIVE, OFF, OFF),
            (ONE_PRIME, TWO, FIVE, OFF, OFF),
        ),

        # NINE => 1,1`,2,5 | 1,3,5 | 1`,3,5
        (
            (ONE, ONE_PRIME, TWO, FIVE, OFF),
            (ONE, THREE, FIVE, OFF, OFF),
            (ONE_PRIME, THREE, FIVE, OFF, OFF),
        ),

        # TEN => 2,3,5 | 1,1`,3,5
        (
            (TWO, THREE, FIVE, OFF, OFF),
            (ONE, ONE_PRIME, THREE, FIVE, OFF),
        ),

        # ELEVEN => 1,2,3,5 | 1`,2,3,5
        (
            (ONE, TWO, THREE, FIVE, OFF),
            (ONE_PRIME, TWO, THREE, FIVE, OFF),
        ),

        # TWELVE => 1,1`,2,3,5
        (
            (ONE, ONE_PRIME, TWO, THREE, FIVE),
        )
    )

    BLACK = ColorFactory.get("black")

    # What color to use from the choosen color_set for each part of the time
    COLOR_HOURS   = 1
    COLOR_MINUTES = 2

    def _tick(self, update_display=False):
        if update_display:
            self.__update_display()

    def __update_display(self):
        (hour, minutes, _) = self._get_hms()

        hour = hour - 12 if hour > 12 else hour
        minutes = int(minutes / 5)

        color_set = self._get_color_set()

        # Which boxes to turn on
        hour_boxes = self.__number_to_boxes(hour)
        min_boxes  = self.__number_to_boxes(minutes)
        # print(hour_boxes)
        # print("----------")
        # print(min_boxes)

        # What color each box should be
        # Default/assume OFF
        box_colors = {
            self.ONE: 0,
            self.ONE_PRIME: 0,
            self.TWO: 0,
            self.THREE: 0,
            self.FIVE: 0
        }

        # Set box colors for hours
        for box in hour_boxes:
            if box is not self.OFF:
                box_colors[box] += self.COLOR_HOURS

        # Set/update box colors for minutes
        for box in min_boxes:
            if box is not self.OFF:
                box_colors[box] += self.COLOR_MINUTES

        # Update display
        for box_name, color_id in box_colors.items():
            box = self.BOXES[box_name]
            color = color_set[color_id-1] if color_id > 0 else self.BLACK

            for loc in box:
                self._matrix.set_rc(loc[0], loc[1], color)

    def __number_to_boxes(self, number):
        choice = None

        choices = self.NUMBER_MAP[number]
        choice = random.choice(choices)
        return choice

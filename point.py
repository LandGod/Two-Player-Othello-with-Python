# Daniel Gold (46043649)
# ICS 32 - Project #5: Othello (Part II)


import math


class Point:

    def __init__(self, frac_x, frac_y):
        """Initializes a Point object using fractional coordinates."""

        self._frac_x = frac_x
        self._frac_y = frac_y

    def frac(self):
        """ Returns the point's location as a fractional value between 0 and 1."""

        return (self._frac_x, self._frac_y)

    def pixel(self, width: float, height: float) -> (int, int):
        """Returns the point as a tuple with the pixel x and pixel y of the canvas"""

        return (int(self._frac_x * width), int(self._frac_y * height))

    def distance(self, p: 'Point') -> float:
        """Returns the distance from this point object to the specified point object as a fraction of canvas size."""

        return math.hypot((self._frac_x - p._frac_x), (self._frac_y - p._frac_y))


def from_frac(frac_x: float, frac_y: float) -> Point:
    """Creates a point object from the specified fractional coordinates"""

    return Point(frac_x, frac_y)


def from_pixel(pixel_x: int, pixel_y: int, width: int, height: int) -> Point:
    """Creates a point object from the specified pixel coordinates and canvas size"""

    return Point(pixel_x / width, pixel_y / height)


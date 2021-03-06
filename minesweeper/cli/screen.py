"""Move, print, color your terminal screen."""
from blessed import Terminal
from .color import Color
from minesweeper.util.point import Point


term = Terminal()


class Screen:
    """
    Wrap around blessed Terminal.

    Commands can be chained togethe, yet result is the same
    Example: scr.setColor(Color.red).print('Hello').setColor(Color.blue).print(' world!')
    """

    def __init__(self):
        """Create screen."""
        self.cursor = Point(0, 0)
        self.color = Color.white

    def clear(self):
        """Clear screen."""
        print(term.clear())

    def print(self, *args, sep=" "):
        """Print something at screen."""
        string = sep.join(map(str, args))
        self.__printLen = len(string)
        print(string)
        return self

    def whip(self):
        """Whips (clears) current line after last printed char."""
        x = self.cursor.x
        self.setCursor(x + self.__printLen)
        self.print(" " * (term.width - self.cursor.x))
        self.setCursor(x)
        return self

    def setCursor(self, x=None, y=None):
        """Set cursor position."""
        try:
            if x is not None:
                self.cursor.x = int(x)
            if y is not None:
                self.cursor.y = int(y)
        except TypeError:
            raise TypeError("Coordinates must be integer")
        print(term.move_xy(self.cursor.x, self.cursor.y), end="")
        return self

    def setColor(self, color, bg=None):
        """Set current color."""
        if color is None:
            return self
        if isinstance(color, str):
            if color is not Color.reset:
                color = Color(color, bg)
                self.color = color
        elif not isinstance(color, Color):
            raise ValueError(
                f"Color is suppose to be str or Color type, not {type(color)}"
            )
        print(color, end="")
        return self

    def drawPixel(self, x, y, pixel=None, color=None):
        """Draw pixel at (x, y) with color."""
        if type(x) is Point:
            x, y, pixel, color = *x, y, pixel
        elif pixel is None:
            raise ValueError("Cannot draw None pixel")
        self.setCursor(x, y)
        self.setColor(color)
        self.print(pixel)
        self.setColor(Color.reset)
        return self

    def __call__(self, color, bg=None):
        """Set color."""
        self.setColor(color, bg)
        return self

    def __getitem__(self, coords):
        """
        Set cursor position and color.

        [x:y:Color]    set x, y and color with slice
        [x, y, Color]  set x, y and color with tuple/list
        [x:y, Color]   set cursor with slice and color with a value
        [[x,y], Color] set cursor with list and color with a value
        [y]            set y with just a number

        Color could be a number
        Some values could be left unused
        """
        if isinstance(coords, slice):
            x, y, color = coords.start, coords.stop, coords.step
        elif isinstance(coords, tuple) or isinstance(coords, list):
            if len(coords) == 3:
                x, y, color = coords
            elif len(coords) == 2:
                if isinstance(coords[0], tuple) or isinstance(coords[0], list):
                    coords, color = coords
                    if len(coords) == 1:
                        x, y = coords, None
                    elif len(coords) == 2:
                        x, y = coords
                    else:
                        raise ValueError("Unsupported length of coordinates")
                elif isinstance(coords[0], slice):
                    x, y, color = coords[0].start, coords[0].stop, coords[1]
                elif type(coords[0]) is Point:
                    x, y, color = *coords[0], coords[1]
                else:
                    x, y, color = *coords, None
            elif len(coords) == 1:
                x, y, color = None, int(coords), None
            else:
                raise ValueError("Unsupported length of coordinates")
        elif type(coords) is Point:
            x, y, color = *coords, None
        elif isinstance(coords, int) or isinstance(coords, float):
            x, y, color = None, int(coords), None
        else:
            raise ValueError("Unsupported value type for coordinates")
        self.setColor(color)
        self.setCursor(x, y)
        return self

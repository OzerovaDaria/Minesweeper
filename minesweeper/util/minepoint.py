#!/usr/bin/env python

"""Description elemets of field."""

from enum import IntEnum


class Value(IntEnum):
    """Values of field items."""

    empty = 0b0000
    one = 0b0001
    two = 0b0010
    three = 0b0011
    four = 0b0100
    five = 0b0101
    six = 0b0110
    seven = 0b0111
    eight = 0b1000
    barrier = 0b1110
    bomb = 0b1111


class Flag(IntEnum):
    """Types of flag for closed cells.

    noflag - unflagged cell,
    guess - mark supposed bomb,
    sure - flag for 100% bomb.
    """

    noflag = 0b00
    guess = 0b01
    sure = 0b10


class Mask(IntEnum):
    """Mask for field cell."""

    closed = 0b00
    pending = 0b11
    opened = 0b01


class MinePoint:
    """Represent point on the field."""

    VFACTOR = 4
    MFACTOR = 2
    FFACTOR = 2
    MSHIFT = VFACTOR
    FSHIFT = VFACTOR + MFACTOR

    VALUE = (0x1 << VFACTOR) - 1
    MASK = ((0x1 << MFACTOR) - 1) << MSHIFT
    FLAG = ((0x1 << FFACTOR) - 1) << FSHIFT

    def __init__(self):
        """Create empty MinePoint."""
        self.__data = 0

    def __rawFlag(self):
        return self.__data & MinePoint.FLAG

    def __rawMask(self):
        return self.__data & MinePoint.MASK

    def __rawValue(self):
        return self.__data & MinePoint.VALUE

    def __clearFlag(self):
        self.__data ^= self.__rawFlag()

    def __clearMask(self):
        self.__data ^= self.__rawMask()

    def __clearValue(self):
        self.__data ^= self.__rawValue()

    @property
    def flag(self):
        """Get flag value of the cell."""
        return self.__rawFlag() >> MinePoint.FSHIFT

    @flag.setter
    def flag(self, flag):
        """Set flag value of the cell."""
        self.__clearFlag()
        self.__data |= (flag << MinePoint.FSHIFT) & MinePoint.FLAG

    @property
    def mask(self):
        """Get mask value of the cell."""
        return self.__rawMask() >> MinePoint.MSHIFT

    @mask.setter
    def mask(self, mask):
        """Set mask value of the cell."""
        self.__clearMask()
        self.__data |= (mask << MinePoint.MSHIFT) & MinePoint.MASK

    @property
    def value(self):
        """Get bombs value of the cell."""
        return self.__rawValue()

    @value.setter
    def value(self, value):
        """Set bombs value of the cell."""
        self.__clearValue()
        self.__data |= value & MinePoint.VALUE

    def __eq__(self, oth):
        """Compare cell to Value, Mask or Flag."""
        if isinstance(oth, Value):
            return self.value == oth
        elif isinstance(oth, Mask):
            return self.mask == oth
        elif isinstance(oth, Flag):
            return self.flag == oth
        raise TypeError(f'Unexpected type {type(oth)} to compare to')

    def set(self, oth):
        """Set cell value, mask or flag."""
        if isinstance(oth, Value):
            self.value = oth
        elif isinstance(oth, Mask):
            self.mask = oth
        elif isinstance(oth, Flag):
            self.flag = oth
        else:
            raise TypeError(f'Unexpected type {type(oth)} to set to')

    def __repr__(self):
        """Show binary value of cell."""
        return bin(self.__data)

    def __str__(self):
        """Convert to value to string."""
        return str(self.value)

#!/usr/bin/env python3
"""Menus for cli minesweeper."""
from .screen import Screen, Color
from blessed import Terminal
from .app import App as CLIAPP
from .box import Box
from minesweeper.util import Point
from minesweeper.logic.field import Field
from minesweeper.logic.gamestat import Stat


KEYS = {
    "up": "w",
    "down": "s",
    "open": " ",
}
OFFSET_START = 2  # head of startmenu
OFFSET_STAT = 8
MENU_WIDTH = 30

screen = Screen()
stat = Stat()
# stat.assignFile("Gamer1")
# stat.readStatistic()


class Menu:
    """Common class for all menus.

    * item_numb - number of menu items
    * items - list of item names
    * field -  field that is used to represent the menu
    """

    def __init__(self, item_numb, items, field):
        """Create abstract menu."""
        self.oldPos = None
        self.pos = Point(0, 0)
        self.box = Box(field.width + 1, field.height + 1, "soft")
        self.item_numb = item_numb
        self.items = items
        self.field = field

    def drawCursor(self, offset):
        """Draw cursor in current position."""
        offset = Point(offset)
        screen.drawPixel(self.pos + offset, ">", Color.white)
        if self.oldPos is not None:
            screen.drawPixel(self.oldPos + offset, " ", Color.white)

    def move(self, direct):
        """Move cursor at certain direction."""
        if self.pos.y + direct.y >= 0 and self.pos.y + direct.y < self.item_numb:
            self.oldPos = Point(self.pos.x, self.pos.y)
            self.pos += direct


class Startmenu(Menu):
    """Start menu. Appear at the beginning."""

    def __init__(self, item_numb, items, field):
        """Inheritance from Menu."""
        Menu.__init__(self, item_numb, items, field)

    def keyAction(self, key):
        """React to key press."""
        if key == KEYS["up"]:
            self.move(Point(0, -1))
        elif key == KEYS["down"]:
            self.move(Point(0, 1))
        elif key == KEYS["open"]:
            if self.pos.y == 0:
                CLIAPP().mainloop()
                exit()
            # elif self.pos.y == 1:
                # statmenu()
            elif self.pos.y == 2:
                settingsmenu()
                pass
            elif self.pos.y == 3:
                screen.setCursor(0, 0)
                screen.clear()
                exit()

    def draw(self):
        """Draw menu."""
        self.box.draw([0, 0])
        self.drawCursor([1, 1 + OFFSET_START])
        screen[2, 1, Color.white].print("Hello, Gamer1!")
        for i, j in zip(
            self.items, range(OFFSET_START, len(self.items) + OFFSET_START)
        ):
            screen[2, 1 + j, Color.white].print(i)


class Statmenu(Menu):
    """Show statistics."""

    def __init__(self, item_numb, items, field):
        """Inheritance from Menu."""
        Menu.__init__(self, item_numb, items, field)

    def keyAction(self, key):
        """React to key press."""
        if key == KEYS["open"]:
            screen.clear()
            startmenu()

    def draw(self):
        """Draw menu."""
        self.box.draw([0, 0])
        self.drawCursor([1, 1 + OFFSET_STAT])
        screen[2, 1, Color.white].print("Gamer1's statistics")
        stat.print()
        for i, j in zip(self.items, range(OFFSET_STAT, len(self.items) + OFFSET_STAT)):
            screen[2, 1 + j, Color.white].print(i)


class Settingsmenu(Menu):
    """Menu for changing settings."""

    def __init__(self, item_numb, items, field):
        """Inheritance from menu."""
        Menu.__init__(self, item_numb, items, field)

    def keyAction(self, key):
        """React to key press."""
        if key == KEYS["up"]:
            self.move(Point(0, -1))
        elif key == KEYS["down"]:
            self.move(Point(0, 1))
        elif key == KEYS["open"]:
            if self.pos.y == 6:
                screen.clear()
                startmenu()

    def draw(self):
        """Draw menu."""
        self.box.draw([0, 0])
        self.drawCursor([1, 1 + OFFSET_START])
        screen[2, 1, Color.white].print("Settings menu")
        for i, j in zip(
            self.items, range(OFFSET_START, len(self.items) + OFFSET_START)
        ):
            screen[2, 1 + j, Color.white].print(i)


def runmenu(namemenu):
    """Run abstract menu."""
    term = Terminal()
    with term.cbreak(), term.hidden_cursor():
        screen.clear()
        namemenu.draw()
        key = ""

        while key != "q":
            key = term.inkey(timeout=3)
            if not key:
                continue
            namemenu.keyAction(key)
            namemenu.draw()
        screen.clear()


def settingsmenu():
    """Run settings menu."""
    settingsmenu_items = [
        "Language",
        "Gamer",
        "Colors",
        "Sounds",
        "Cursor",
        "Keys",
        "Exit",
    ]
    settingsfield = Field(MENU_WIDTH, len(settingsmenu_items) + OFFSET_START, 0.15)
    settingsmenu = Settingsmenu(
        len(settingsmenu_items), settingsmenu_items, settingsfield
    )
    runmenu(settingsmenu)


def statmenu():
    """Run statmenu menu."""
    statmenu_items = ["Exit"]
    statfield = Field(MENU_WIDTH, len(statmenu_items) + OFFSET_STAT, 0.15)
    statmenu = Statmenu(len(statmenu_items), statmenu_items, statfield)
    runmenu(statmenu)


def startmenu():
    """Run startmenu menu."""
    startmenu_items = ["Game", "Statistics", "Settings", "Exit"]
    startfield = Field(MENU_WIDTH, len(startmenu_items) + OFFSET_START, 0.15)
    startmenu = Startmenu(len(startmenu_items), startmenu_items, startfield)
    runmenu(startmenu)

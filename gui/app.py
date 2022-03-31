"""Main GUI module that draw all the game attributes."""

import tkinter as tk
from .board import Board


class App(tk.Tk):
    def __init__(self, width=900, height=900):
        super().__init__()
        self.title = 'Minesweeper'
        self.canvas = tk.Canvas(self, width=width, height=width, bg="#ffffff")
        self.canvas.pack(expand='no', fill='both')

        self.board = Board(self, 12)
"""Main GUI module that draw all the game attributes."""

import tkinter as tk
from .game import Game
from .colors import COLORS
from .events import EventMaster
from .menu import MainMenu, NewGameMenu, SettingsMenu
import configparser
from translation import setLang
# from tkextrafont import Font


class App(tk.Tk):
    """Gui App class."""

    def __init__(self):
        """Initialize GUI app."""
        super().__init__()
        EventMaster(self)
        self.title = 'Minesweeper'
        self.username = 'Gamer1'

        # self.fontLoaded = Font(file="./resources/fonts/Purisa_Bold.ttf", size=20, family='Purisa')
        self.font = ('Purisa', 20)
        # self.font = ('Default', 20)

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.appOpts = self.config['settings']

        if self.appOpts['fullscreen'] == 'True':
            self.setFullscreen()
        self.width, self.height = map(int, self.appOpts['resolution'].split('x'))
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.onDeath)
        self.bind("<<Switch-Menu>>", self.switchMenu)
        self.bind("<<Start-Game>>", self.onGameInit)
        self.bind("<<Save-Settings>>", self.onSettingsSave)

        self.page = 'MainMenu'
        self.gameOpts = { 'difficulty': 0.1, 'fieldsize-name': 0 }

        COLORS.setTheme(self.appOpts['colorscheme'])
        self.configure(bg=COLORS['main'],)

        self.session = None
        self.newSession()

    def onDeath(self):
        """Application is closed."""
        # print('App is dying')
        self.destroy()

    def setFullscreen(self):
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        self.appOpts['resolution'] = f'{screenWidth}x{screenHeight}'
        self.attributes('-fullscreen', True)

    def onSettingsSave(self, event):
        """Save settings given from menu."""
        self.appOpts = event.data

        COLORS.setTheme(self.appOpts['colorscheme'])
        self.configure(bg=COLORS['main'])

        if self.appOpts['fullscreen'] == 'True':
            self.setFullscreen()
        else:
            self.attributes('-fullscreen', False)
        self.geometry(self.appOpts['resolution'])
        self.width, self.height = map(int, event.data['resolution'].split('x'))

        setLang(self.appOpts['language'])

        self.config['settings'] = self.appOpts
        with open('config.ini', 'w') as configFile:
            self.config.write(configFile)

    def onGameInit(self, event):
        """Init game with given options by menu."""
        self.gameOpts = event.data
        self.page = 'Game'
        self.newSession()

    def switchMenu(self, event):
        """Switch current view to given menu."""
        # print('Asked to switch menu to', event)
        if event.data != self.page:
            self.page = event.data
            self.newSession()

    def newSession(self, args=None):
        """Replace current view with new session based on self.page."""
        if self.session:
            self.session.destroy()
            self.session = None

        if self.page == 'MainMenu':
            self.session = MainMenu(self)
        elif self.page == 'NewGameMenu':
            self.session = NewGameMenu(self, self.username)
        elif self.page == 'SettingsMenu':
            self.session = SettingsMenu(self)
        elif self.page == 'Game':
            self.session = Game(
                self,
                self.gameOpts['fieldsize'],
                self.gameOpts['difficulty']
            )

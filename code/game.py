import pygame as pg  # ctr + alt + l (formatar pep8)
from code.menu import Menu
from code.Const import WIN_WIDTH, WIN_HEIGHT


class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        while True:
            menu = Menu(self.window)
            menu.run()
            pass

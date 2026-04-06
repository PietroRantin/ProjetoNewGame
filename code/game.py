import pygame as pg  # ctr + alt + l (formatar pep8)
from code.menu import Menu


class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode(size=(640, 480))

    def run(self):
        while True:
            menu = Menu(self.window)
            menu.run()
            pass

            # Check for all events
            # for event in pg.event.get():
            #     if event.type == pg.QUIT:
            #         pg.quit()  # Close Window
            #         quit()  # End Pygame

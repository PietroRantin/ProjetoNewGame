import pygame as pg  # ctr + alt + l (formatar pep8)

from code.level import Level
from code.menu import Menu
from code.Const import WIN_WIDTH, WIN_HEIGHT, COLOR_WHITE

class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def show_gameover(self):
        # Tela simples de game over — aperta qualquer tecla para voltar ao menu
        font = pg.font.SysFont('Lucida Sans Typewriter', 40)
        small_font = pg.font.SysFont('Lucida Sans Typewriter', 20)

        while True:
            self.window.fill((0, 0, 0))

            text = font.render('GAME OVER', True, COLOR_WHITE)
            sub = small_font.render('Pressione qualquer tecla para voltar', True, COLOR_WHITE)

            self.window.blit(text, text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 30)))
            self.window.blit(sub, sub.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 20)))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    return 'menu'

            pg.display.flip()

    def run(self):
        state = 'menu'

        while True:
            if state == 'menu':
                menu = Menu(self.window)
                state = menu.run()

            elif state == 'game':
                level = Level(self.window)
                state = level.run()

            elif state == 'gameover':
                state = self.show_gameover()

            elif state == 'score':
                state = 'menu'
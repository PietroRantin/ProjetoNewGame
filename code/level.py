import pygame as pg
from code.Const import WIN_WIDTH, WIN_HEIGHT, COLOR_WHITE
from code.player import Player


class Level:
    def __init__(self, window):
        self.window = window
        self.clock = pg.time.Clock()

        # Altura do chão
        self.ground_y = WIN_HEIGHT - 20

        self.player = Player(self.window)

    def run(self):
        while True:
            # Limpa a tela com cor preta
            self.window.fill((0, 0, 0))

            # Eventos
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return 'menu'
                    if event.key == pg.K_SPACE:
                        self.player.jump()

            # Atualiza e desenha o chão
            pg.draw.rect(self.window, COLOR_WHITE, (0, self.ground_y, WIN_WIDTH, 20))

            # Atualiza e desenha o player
            self.player.update(self.ground_y)
            self.player.draw()

            pg.display.flip()
            self.clock.tick(60)  # limita a 60 FPS

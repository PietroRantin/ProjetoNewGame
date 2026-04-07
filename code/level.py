import pygame as pg
from code.Const import WIN_WIDTH, WIN_HEIGHT, COLOR_WHITE
from code.platform import PlataformManager
from code.player import Player
from code.background import Background


class Level:
    def __init__(self, window):
        self.window = window
        self.clock = pg.time.Clock()

        # Altura do chão
        self.ground_y = WIN_HEIGHT - 20

        # Camadas de background com velocidades diferentes (parallax)
        # substitui os caminhos pelas suas imagens reais
        self.backgrounds = [
            Background(self.window, './asset/bg_far1.png', 0.3),  # lua/estrelas - lenta
            Background(self.window, './asset/bg_far3.png', 0.8, True),  # nuvens - média
            Background(self.window, './asset/bg_close1.png', 2.0, True),  # primeiro plano - rápida
        ]

        self.scroll_speed = 3 # Velocidade Global do scroll
        self.platform_manager = PlataformManager(self.scroll_speed)
        self.player = Player(self.window)

    def run(self):
        while True:
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

            # Ordem do desenho: fundo - chão - player
            for bg in self.backgrounds:
                bg.update()
                bg.draw()

            # Plataformas
            self.platform_manager.update()
            self.platform_manager.draw(self.window)

            # Chão
            pg.draw.rect(self.window, COLOR_WHITE, (0, self.ground_y, WIN_WIDTH, 20))

            # Player
            self.player.update(self.ground_y, self.platform_manager.get_platforms())
            self.player.draw()

            pg.display.flip()
            self.clock.tick(60)  # limita a 60 FPS

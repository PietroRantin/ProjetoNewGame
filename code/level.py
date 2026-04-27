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

    def check_death(self):
        if self.player.is_fallen():
            self.player.take_damege()

            if not self.player.alive:
                return 'game over'

            self.player.x = 100
            self.player.y = WIN_HEIGHT - 100
            self.player.vel_y = 0

        return None

    def draw_hud(self):
        # HUD simples: vidas no canto superior esquerdo
        font = pg.font.SysFont('Lucida Sans Typewriter', 18)
        lives_text = font.render(f'Vidas: {self.player.lives}', True, COLOR_WHITE)
        self.window.blit(lives_text, (10, 10))


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
                        self.player.request_jump()

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

            # Checa morte depois de atualizar o player
            result = self.check_death()
            if result:
                return result  # → 'gameover'

            self.draw_hud()

            pg.display.flip()
            self.clock.tick(60)
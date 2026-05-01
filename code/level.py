import pygame as pg
from code.Const import WIN_WIDTH, WIN_HEIGHT, COLOR_WHITE
from code.player import Player
from code.background import Background
from code.platform import Platform, PlataformManager


class Level:
    def __init__(self, window):
        self.window = window
        self.clock = pg.time.Clock()

        self.backgrounds = [
            Background(self.window, './asset/bg_far1.png', 0.3),
            Background(self.window, './asset/bg_far3.png', 0.8, True),
            Background(self.window, './asset/bg_close1.png', 2.0, True),
        ]

        self.scroll_speed = 3
        self.platform_manager = PlataformManager(self.scroll_speed)
        # Spawn platform ANTES do player
        spawn_y = WIN_HEIGHT - 80
        self.spawn_platform = Platform(0, spawn_y, WIN_WIDTH // 2, scroll_speed=0)
        self.spawn_timer = 180 # 3 segundos a 60fps

        # Player criado UMA vez, posicionado em cima da spawn
        self.player = Player(self.window, start_y=self.spawn_platform.rect.top)

    def get_all_platforms(self):
        platforms = self.platform_manager.get_platforms()
        # Só inclui a spawn platform se ainda estiver ativa
        if self.spawn_timer > 0:
            platforms = [self.spawn_platform] + platforms
        return platforms

    def update_spawn_platform(self):
        if self.spawn_timer > 0:
            self.spawn_timer -= 1

    def draw_spawn_platform(self):
        if self.spawn_timer > 0:
            # Pisca nos últimos 60 frames (1 segundo) para avisar que vai sumir
            if self.spawn_timer > 60 or (self.spawn_timer // 6) % 2 == 0:
                self.spawn_platform.draw(self.window)

    def get_respawn_platform(self):
        platforms = self.platform_manager.get_platforms()

        if not platforms:
            return None

        # Pega a plataforma mais à esquerda que ainda está visível na tela
        visible = [p for p in platforms if p.x + p.width > 0 and p.x < WIN_WIDTH]

        if not visible:
            return visible[0] if platforms else None

        # Prefere a plataforma mais à esquerda (mais próxima do player)
        return min(visible, key=lambda p: p.x)

    def check_death(self):
        if self.player.is_fallen():
            self.player.take_damage()

            if not self.player.alive:
                return 'gameover'

            # Tenta reaparecer na spawn (se ainda ativa) ou na plataforma mais próxima
            if self.spawn_timer > 0:
                self.player.respawn(
                    x=100,
                    y=self.spawn_platform.rect.top - self.player.height
                )
            else:
                plat = self.get_respawn_platform()
                if plat:
                    self.player.respawn(
                        x=plat.x + 20,
                        y=plat.rect.top - self.player.height
                    )
                else:
                    # Nenhuma plataforma visível — reaparecer no topo da tela
                    # e deixar o jogador cair naturalmente sobre o que vier
                    self.player.respawn(
                        x=100,
                        y=50
                    )

        return None

    def draw_hud(self):
        font = pg.font.SysFont('Lucida Sans Typewriter', 18)
        lives_text = font.render(f'Vidas: {self.player.lives}', True, COLOR_WHITE)
        self.window.blit(lives_text, (10, 10))

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return 'menu'
                    if event.key == pg.K_SPACE:
                        self.player.request_jump()

            for bg in self.backgrounds:
                bg.update()
                bg.draw()

            # Spawn platform (não chama update — ela não se move)
            self.update_spawn_platform()
            self.draw_spawn_platform()

            self.platform_manager.update()
            self.platform_manager.draw(self.window)

            # Passa todas as plataformas juntas para o player
            self.player.update(self.get_all_platforms())
            self.player.draw()

            result = self.check_death()
            if result:
                return result

            self.draw_hud()

            pg.display.flip()
            self.clock.tick(60)
            print(f'spawn rect: {self.spawn_platform.rect}  |  player y: {self.player.y}  |  on_ground: {self.player.on_ground}')
import pygame as pg
from code.player import Player
from code.background import Background
from code.platform import Platform, PlataformManager
from code.enemy import EnemyManager
from code.Const import WIN_WIDTH, WIN_HEIGHT, COLOR_WHITE, SCORE_TO_WIN
from code.score_manager import save_score


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
        self.enemy_manager = EnemyManager(self.scroll_speed)

        spawn_y = WIN_HEIGHT - 80
        self.spawn_platform = Platform(0, spawn_y, WIN_WIDTH // 2, scroll_speed=0)
        self.spawn_timer = 180

        self.player = Player(self.window, start_y=self.spawn_platform.rect.top)

        # Pontuação
        self.score = 0

    def get_all_platforms(self):
        platforms = self.platform_manager.get_platforms()
        if self.spawn_timer > 0:
            platforms = [self.spawn_platform] + platforms
        return platforms

    def update_spawn_platform(self):
        if self.spawn_timer > 0:
            self.spawn_timer -= 1

    def draw_spawn_platform(self):
        if self.spawn_timer > 0:
            if self.spawn_timer > 60 or (self.spawn_timer // 6) % 2 == 0:
                self.spawn_platform.draw(self.window)

    def check_enemy_collision(self):
        player_rect = self.player.get_rect()

        for enemy in self.enemy_manager.get_enemies():
            if not player_rect.colliderect(enemy.rect):
                continue

            if (self.player.vel_y > 0 and
                    player_rect.bottom - self.player.vel_y <= enemy.rect.top + 6):
                self.enemy_manager.enemies.remove(enemy)
                self.player.kill_enemy_bounce()
                self.score += 100
            else:
                self.player.take_damage()
                if not self.player.alive:
                    return 'gameover'  # ← retorna estado

        return None

    def get_respawn_platform(self):
        platforms = self.platform_manager.get_platforms()
        if not platforms:
            return None
        visible = [p for p in platforms if p.x + p.width > 0 and p.x < WIN_WIDTH]
        if not visible:
            return platforms[0] if platforms else None
        return min(visible, key=lambda p: p.x)

    def check_death(self):
        if self.player.is_fallen():
            self.player.take_damage()

            if not self.player.alive:
                return 'gameover'

            if self.spawn_timer > 0:
                self.player.respawn(x=100,
                                    y=self.spawn_platform.rect.top - self.player.height)
            else:
                plat = self.get_respawn_platform()
                if plat:
                    self.player.respawn(x=plat.x + 20,
                                        y=plat.rect.top - self.player.height)
                else:
                    self.player.respawn(x=100, y=50)

        return None

    def draw_hud(self):
        font = pg.font.SysFont('Lucida Sans Typewriter', 18)

        lives_text = font.render(f'Vidas: {self.player.lives}', True, COLOR_WHITE)
        self.window.blit(lives_text, (10, 10))

        score_text = font.render(f'Score: {self.score}', True, COLOR_WHITE)
        # Score no canto superior direito
        self.window.blit(score_text, (WIN_WIDTH - score_text.get_width() - 10, 10))

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return 'menu', self.score
                    if event.key == pg.K_SPACE:
                        self.player.request_jump()

            for bg in self.backgrounds:
                bg.update()
                bg.draw()

            self.update_spawn_platform()
            self.draw_spawn_platform()

            self.platform_manager.update()
            self.platform_manager.draw(self.window)

            # Passa plataformas para o enemy manager também (para o spawn)
            self.enemy_manager.update(self.platform_manager.get_platforms())
            self.enemy_manager.draw(self.window)

            self.player.update(self.get_all_platforms())
            self.player.draw()

            # Checa colisões nesta ordem — inimigo antes de morte
            result = self.check_enemy_collision()  # ← captura
            if result:
                return result, self.score

            result = self.check_death()
            if result:
                return result, self.score

            # Pontuação por sobrevivência
            self.score += 1

            if self.score >= SCORE_TO_WIN:
                save_score(self.score)
                return 'victory', self.score

            self.draw_hud()

            pg.display.flip()
            self.clock.tick(60)
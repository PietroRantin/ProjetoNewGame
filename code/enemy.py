import pygame as pg
import random
from code.Const import WIN_WIDTH, WIN_HEIGHT, COLOR_WHITE


class Enemy:
    def __init__(self, x, y, scroll_speed):
        self.width = 28
        self.height = 28
        self.x = x
        self.y = y
        self.scroll_speed = scroll_speed
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        # Carrega e redimensiona o sprite
        self.sprite = self._load_sprite()

    def _load_sprite(self):
        img = pg.image.load('./asset/inimigo.png').convert_alpha()
        return pg.transform.scale(img, (self.width, self.height))

    def update(self):
        self.x -= self.scroll_speed
        self.rect.x = self.x

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))

    def off_screen(self):
        return self.x + self.width < 0


class EnemyManager:
    def __init__(self, scroll_speed):
        self.scroll_speed = scroll_speed
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 180  # tenta spawnar a cada 3 segundos

    def try_spawn(self, platforms):
        # Só spawna em plataformas fora da tela (à direita)
        valid = [p for p in platforms if p.x > WIN_WIDTH]

        if not valid:
            return

        # Escolhe plataforma aleatória dentre as válidas
        plat = random.choice(valid)

        # Posiciona o inimigo em cima da plataforma
        enemy_x = plat.x + random.randint(10, max(11, plat.width - 40))
        enemy_y = plat.rect.top - 28  # 28 = altura do inimigo

        self.enemies.append(Enemy(enemy_x, enemy_y, self.scroll_speed))

    def update(self, platforms):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.try_spawn(platforms)

        for enemy in self.enemies:
            enemy.update()

        # Remove inimigos fora da tela
        self.enemies = [e for e in self.enemies if not e.off_screen()]

    def draw(self, window):
        for enemy in self.enemies:
            enemy.draw(window)

    def get_enemies(self):
        return self.enemies
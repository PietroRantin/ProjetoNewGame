import pygame as pg
import random
from code.Const import WIN_WIDTH, WIN_HEIGHT, COLOR_WHITE


class Platform:
    def __init__(self, x, y, width, scroll_speed):
        self.width = width
        self.height = 16  # plataforma
        self.x = x
        self.y = y
        self.scroll_speed = scroll_speed
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x -= self.scroll_speed
        self.rect.x = self.x  # atualiza o rect

    def draw(self, window):
        pg.draw.rect(window, COLOR_WHITE, self.rect)

    def off_screen(self):
        return self.x + self.width < 0 # saiu pela esquerda

class PlataformManager:
    def __init__(self, scroll_speed):
        self.scroll_speed = scroll_speed
        self.platforms = []

        # Gera plataformas iniciais para a tela não começar vazia
        self._generate_initial()

    def _generate_initial(self):
        x = 300  # começa um pouco à frente do player
        while x < WIN_WIDTH + 200:
            plat = self._create_platform(x)
            self.platforms.append(plat)
            x += plat.width + random.randint(80, 200)

    def _create_platform(self, x):
        width = random.randint(100, 220)

        # Y entre 55% e 80% da altura da tela — faixa jogável
        min_y = int(WIN_HEIGHT * 0.45)
        max_y = int(WIN_HEIGHT * 0.78)
        y = random.randint(min_y, max_y)

        return Platform(x, y, width, self.scroll_speed)

    def update(self):
        for plat in self.platforms:
            plat.update()

        # Remove plataformas que saíram da tela
        self.platforms = [p for p in self.platforms if not p.off_screen()]

        # Gera nova plataforma quando a última está chegando perto da borda direita
        if self.platforms:
            last = self.platforms[-1]
            if last.x + last.width < WIN_WIDTH + 100:
                new_x = max(last.x + last.width + random.randint(80, 200), WIN_WIDTH)
                self.platforms.append(self._create_platform(new_x))

    def draw(self, window):
        for plat in self.platforms:
            plat.draw(window)

    def get_platforms(self):
        return self.platforms

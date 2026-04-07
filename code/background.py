import pygame as pg
from code.Const import WIN_WIDTH, WIN_HEIGHT


class Background:
    def __init__(self, window, image_path, scroll_speed, transparent=False):
        self.window = window
        self.image = pg.image.load(image_path).convert()

        # Redimensiona para cobrir a tela inteira
        self.image = pg.transform.scale(self.image, (WIN_WIDTH, WIN_HEIGHT))

        # Preto fica transparente para as camadas sobrepostas
        if transparent:
            self.image.set_colorkey((0, 0, 0))

        self.scroll_speed = scroll_speed
        self.x = 0  # Posição atual do scroll

    def update(self):
        # Move a imagem para a esquerda
        self.x -= self.scroll_speed

        # Reseta quando a imagem sair por completo
        if self.x <= -WIN_WIDTH:
            self.x = 0

    def draw(self):
        # Desenha duas copias lado a lado
        self.window.blit(self.image, (self.x, 0))
        self.window.blit(self.image, (self.x + WIN_WIDTH, 0))

from idlelib import window

import pygame as pg
from code.Const import WIN_HEIGHT, COLOR_WHITE


class Player:
    def __init__(self, window):
        self.window = window

        # Posição e tamanho
        self.width = 28
        self.height = 32
        self.x = 100
        self.y = WIN_HEIGHT - 100  # Começando proximo ao chão

        # Física
        self.vel_y = 0
        self.gravity = 0.6
        self.jump_force = -13
        self.on_ground = False

        # Velocidade Horizontal
        self.vel_x = 0

    def handle_input(self):
        keys = pg.key.get_pressed()

        # Move Horizontal
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel_x = -5
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel_x = 5
        else:
            self.vel_x = 0

    def jump(self):
        if self.on_ground:  # Só pula se estiver no chão
            self.vel_y = self.jump_force
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += self.gravity

        # Limite (evita atravessar plataformas em alta velocidade)
        if self.vel_y > 15:
            self.vel_y = 15

    def update(self, ground_y):
        self.handle_input()
        self.apply_gravity()

        # Aplica movimento
        self.x += self.vel_x
        self.y += self.vel_y

        # Colisão com o chão
        if self.y >= ground_y - self.height:
            self.y = ground_y - self.height
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def draw(self):
        # Retângulo colorido (substituir por sprite depois)
        pg.draw.rect(
            self.window,
            COLOR_WHITE,
            (self.x, self.y, self.width, self.height)
        )

    def get_rect(self):
        return pg.Rect(self.x, self.y, self.width, self.height)

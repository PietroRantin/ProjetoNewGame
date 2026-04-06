#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame as pg
from pygame import Rect, Surface
from pygame.font import Font

from code.Const import WIN_WIDTH


class Menu:
    def __init__(self, window):
        self.window = window
        self.surface = pg.image.load('./asset/MenuBG.png')
        self.rect = self.surface.get_rect(left=0, top=0)
        self.font = {}
        self.text_cache = {}

    def run(self):
        pg.mixer_music.load('./asset/GameMusic.wav')
        pg.mixer_music.play(-1)

        while True:
            self.window.blit(source=self.surface, dest=self.rect)
            self.menu_text(50, "DreadFul", (240, 240, 255), ((WIN_WIDTH / 2), 40))
            self.menu_text(50, "Nugget", (240, 240, 255), ((WIN_WIDTH / 2), 90))
            pg.display.flip()

            # Check for all events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()  # Close Window
                    quit()  # End Pygame

    def get_font(self, size):
        if size not in self.font:
            self.font[size] = pg.font.SysFont('Lucida Sans Typewriter', size)
        return self.font[size]

    def render_text_with_outline(self, text, size, text_color, outline_color=(0, 0, 0), outline_width=2):
        key = (text, size, text_color, outline_color, outline_width)

        # Cache: evita recriar tudo
        if key in self.text_cache:
            return self.text_cache[key]

        font = self.get_font(size)

        # Texto base
        text_surf = font.render(text, True, text_color).convert_alpha()

        # Criar superfície maior (pra caber a borda)
        w, h = text_surf.get_size()
        outline_surf = pg.Surface((w + outline_width * 2, h + outline_width * 2), pg.SRCALPHA)

        # Desenhar borda (em volta)
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    outline = font.render(text, True, outline_color)
                    outline_surf.blit(outline, (dx + outline_width, dy + outline_width))

        # Desenhar texto principal no centro
        outline_surf.blit(text_surf, (outline_width, outline_width))

        # Salvar no cache
        self.text_cache[key] = outline_surf

        return outline_surf

    def menu_text(self, text_size, text, text_color, text_center_pos):
        text_surface = self.render_text_with_outline(
            text=text,
            size=text_size,
            text_color=text_color,
            outline_color=(0, 0, 0),
            outline_width=1
        )

        rect = text_surface.get_rect(center=text_center_pos)
        self.window.blit(text_surface, rect)

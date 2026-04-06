import pygame as pg
from code.Const import WIN_WIDTH, COLOR_TITLE, COLOR_WHITE


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
            clicked = False

            self.window.blit(source=self.surface, dest=self.rect)

            # Titulo
            self.menu_text(50, "DreadFul", COLOR_TITLE, ((WIN_WIDTH / 2), 40))
            self.menu_text(50, "Nigths", COLOR_TITLE, ((WIN_WIDTH / 2), 90))

            # Check for all events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()  # Close Window
                    quit()  # End Pygame
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    clicked = True

            # Botões
            self.draw_button("New Game", 20, (WIN_WIDTH / 2, 200), self.start_game, clicked)
            self.draw_button("Score", 20, (WIN_WIDTH / 2, 250), self.show_score, clicked)

            pg.display.flip()


    def start_game(self):
        print('Iniciando o jogo...')
        # Troca de telas depois

    def show_score(self):
        print('Mostrando os scores...')

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

    def draw_button(self, text, size, center_pos, action=None, clicked=False):
        mouse_pos = pg.mouse.get_pos()

        # Render do Texto com borda (usa funcao ja otimizada)
        text_surf = self.render_text_with_outline(
            text=text,
            size=size,
            text_color=COLOR_WHITE,
            outline_color=(0, 0, 0),
            outline_width=3
        )

        text_rect = text_surf.get_rect(center=center_pos)

        # Area do Botao (padding :/)
        padding_x, padding_y = 20, 10
        button_rect = pg.Rect(
            text_rect.left - padding_x,
            text_rect.top - padding_y,
            text_rect.width + padding_x * 2,
            text_rect.height + padding_y * 2
        )

        # Hover effect
        if button_rect.collidepoint(mouse_pos):
            collor = COLOR_WHITE
            border = (250,250,250)

            # clique
            if clicked and action:
                action()
        else:
            collor = (200, 200, 200)
            border = (0,0,0)

        # Fundo do Botão (teste 1-bit)
        pg.draw.rect(self.window, border, button_rect, 2)

        # Texto
        self.window.blit(text_surf, text_rect)





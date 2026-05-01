import pygame as pg
from code.menu import Menu
from code.level import Level
from code.score_manager import save_score
from code.score_screen import ScoreScreen
from code.Const import WIN_WIDTH, WIN_HEIGHT, COLOR_WHITE, COLOR_TITLE


class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.last_score = None  # guarda score entre telas

    def show_gameover(self):
        font = pg.font.SysFont('Lucida Sans Typewriter', 40)
        small_font = pg.font.SysFont('Lucida Sans Typewriter', 18)

        while True:
            self.window.fill((0, 0, 0))

            text = font.render('GAME OVER', True, COLOR_WHITE)
            sub = small_font.render(
                f'Score final: {self.last_score}', True, COLOR_WHITE)
            back = small_font.render(
                'Pressione qualquer tecla para voltar', True, (150, 150, 150))

            self.window.blit(text, text.get_rect(
                center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 40)))
            self.window.blit(sub, sub.get_rect(
                center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 10)))
            self.window.blit(back, back.get_rect(
                center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 40)))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    return 'menu'

            pg.display.flip()

    def show_victory(self):
        font = pg.font.SysFont('Lucida Sans Typewriter', 40)
        small_font = pg.font.SysFont('Lucida Sans Typewriter', 18)

        while True:
            self.window.fill((0, 0, 0))

            text = font.render('VOCÊ VENCEU!', True, (255, 215, 0))
            sub = small_font.render(
                f'Score: {self.last_score}', True, COLOR_WHITE)
            back = small_font.render(
                'Pressione qualquer tecla para ver o ranking', True, (150, 150, 150))

            self.window.blit(text, text.get_rect(
                center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 40)))
            self.window.blit(sub, sub.get_rect(
                center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 10)))
            self.window.blit(back, back.get_rect(
                center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 40)))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    return 'score'

            pg.display.flip()

    def run(self):
        state = 'menu'

        while True:
            if state == 'menu':
                menu = Menu(self.window)
                state = menu.run()

            elif state == 'game':
                level = Level(self.window)
                state, self.last_score = level.run()  # ← recebe score junto

            elif state == 'gameover':
                save_score(self.last_score)  # salva mesmo perdendo
                state = self.show_gameover()

            elif state == 'victory':
                state = self.show_victory()

            elif state == 'score':
                score_screen = ScoreScreen(self.window, self.last_score)
                state = score_screen.run()
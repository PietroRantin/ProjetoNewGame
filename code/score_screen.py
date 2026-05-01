import pygame as pg
from code.Const import WIN_WIDTH, WIN_HEIGHT, COLOR_WHITE, COLOR_TITLE
from code.score_manager import load_scores


class ScoreScreen:
    def __init__(self, window, last_score=None):
        self.window = window
        self.last_score = last_score  # score da partida atual (pode ser None)
        self.font_big = pg.font.SysFont('Lucida Sans Typewriter', 36)
        self.font_mid = pg.font.SysFont('Lucida Sans Typewriter', 22)
        self.font_small = pg.font.SysFont('Lucida Sans Typewriter', 16)

    def run(self):
        scores = load_scores()

        while True:
            self.window.fill((0, 0, 0))

            # Título
            title = self.font_big.render('MELHORES SCORES', True, COLOR_TITLE)
            self.window.blit(title, title.get_rect(center=(WIN_WIDTH // 2, 40)))

            # Score da partida atual
            if self.last_score is not None:
                current = self.font_mid.render(
                    f'Seu score: {self.last_score}', True, COLOR_WHITE)
                self.window.blit(current, current.get_rect(center=(WIN_WIDTH // 2, 85)))

            # Lista dos top scores
            if scores:
                for i, score in enumerate(scores):
                    # Destaca o primeiro lugar
                    color = (255, 215, 0) if i == 0 else COLOR_WHITE
                    prefix = '>> ' if i == 0 else f'{i + 1}.  '
                    text = self.font_mid.render(f'{prefix}{score}', True, color)
                    self.window.blit(text, text.get_rect(
                        center=(WIN_WIDTH // 2, 130 + i * 35)))
            else:
                empty = self.font_small.render(
                    'Nenhum score salvo ainda.', True, COLOR_WHITE)
                self.window.blit(empty, empty.get_rect(center=(WIN_WIDTH // 2, 150)))

            # Instrução
            back = self.font_small.render(
                'Pressione qualquer tecla para voltar', True, (150, 150, 150))
            self.window.blit(back, back.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 20)))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    return 'menu'

            pg.display.flip()
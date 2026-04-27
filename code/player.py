import pygame as pg
from code.Const import WIN_HEIGHT, COLOR_WHITE

# Constantes de tuning — fácil de ajustar
COYOTE_FRAMES = 6    # frames de graça após sair da plataforma
JUMP_BUFFER_FRAMES = 8  # frames que o jogo "lembra" do botão de pulo
GROUND_TOLERANCE = 4    # pixels de margem na detecção de chão
INVINCIBLE_FRAMES = 90


class Player:
    def __init__(self, window):
        self.window = window
        self.width = 28
        self.height = 30
        self.x = 100
        self.y = WIN_HEIGHT - 100

        self.vel_y = 0
        self.gravity = 0.7
        self.jump_force = -14
        self.on_ground = False
        self.vel_x = 0

        # Contadores para coyote time e jump buffer
        self.coyote_timer = 0
        self.jump_buffer_timer = 0

        # Sistema de vidas
        self.lives = 3
        self.invincible_timer = 0
        self.alive = True

    def take_damege(self):
        if self.invincible_timer > 0:
            return

        self.lives -= 1
        self.invincible_timer = INVINCIBLE_FRAMES

        if self.lives <= 0:
            self.alive = False

    def is_fallen(self):
        return self.y > WIN_HEIGHT + 50

    def handle_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel_x = -4
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel_x = 4
        else:
            self.vel_x = 0

    def request_jump(self):
        # Chamado pelo KEYDOWN — registra a intenção de pular
        self.jump_buffer_timer = JUMP_BUFFER_FRAMES

    def try_jump(self):
        # Executa o pulo se há intenção E condição (chão ou coyote time)
        can_jump = self.on_ground or self.coyote_timer > 0
        wants_jump = self.jump_buffer_timer > 0

        if can_jump and wants_jump:
            self.vel_y = self.jump_force
            self.on_ground = False
            self.coyote_timer = 0      # consome o coyote time
            self.jump_buffer_timer = 0  # consome o buffer

    def apply_gravity(self):
        self.vel_y += self.gravity
        if self.vel_y > 15:
            self.vel_y = 15

    def check_platform_collision(self, platforms):
        was_on_ground = self.on_ground
        self.on_ground = False
        player_rect = self.get_rect()

        for plat in platforms:
            if player_rect.colliderect(plat.rect):
                if self.vel_y >= 0 and player_rect.bottom - self.vel_y <= plat.rect.top + GROUND_TOLERANCE:
                    self.y = plat.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    break

        # Coyote time: estava no chão, agora não está mais → inicia contagem
        if was_on_ground and not self.on_ground:
            self.coyote_timer = COYOTE_FRAMES

    def update_timers(self):
        # Decrementa os timers a cada frame (nunca abaixo de zero)
        if self.coyote_timer > 0:
            self.coyote_timer -= 1
        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= 1

    def update(self, ground_y, platforms=None):
        self.handle_input()
        self.apply_gravity()

        self.x += self.vel_x
        self.y += self.vel_y

        if platforms:
            self.check_platform_collision(platforms)

        # Chão principal
        if self.y >= ground_y - self.height:
            self.y = ground_y - self.height
            self.vel_y = 0
            self.on_ground = True

        # Tenta executar pulo (depois de atualizar on_ground)
        self.try_jump()

        # Atualiza contadores
        self.update_timers()

    def draw(self):
        pg.draw.rect(self.window, COLOR_WHITE, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pg.Rect(self.x, self.y, self.width, self.height)
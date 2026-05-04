import pygame as pg
from code.Const import WIN_HEIGHT, COLOR_WHITE

COYOTE_FRAMES = 6
JUMP_BUFFER_FRAMES = 8
GROUND_TOLERANCE = 4
INVINCIBLE_FRAMES = 90
ANIM_SPEED = 6  # frames do jogo por frame de animação


class Player:
    def __init__(self, window, start_y=None):
        self.window = window
        self.width = 28
        self.height = 30
        self.x = 100

        if start_y is not None:
            self.y = start_y - self.height
        else:
            self.y = WIN_HEIGHT - 150

        self.vel_y = 0
        self.gravity = 0.7
        self.jump_force = -14
        self.on_ground = False
        self.vel_x = 0

        self.coyote_timer = 0
        self.jump_buffer_timer = 0

        self.lives = 3
        self.invincible_timer = 0
        self.alive = True

        # Animação
        self.sprites_run = self._load_run_frames()
        self.sprite_idle = self._load_sprite('./asset/player_PARADO.png')
        self.anim_index = 0    # qual frame da animação está ativo
        self.anim_timer = 0    # contador de frames do jogo

        self.facing_right = True  # controla direção do sprite

    def _load_sprite(self, path):
        img = pg.image.load(path).convert_alpha()
        return pg.transform.scale(img, (self.width, self.height))

    def _load_run_frames(self):
        frames = []
        for i in range(2, 7):  # player_2 até player_6
            img = pg.image.load(f'./asset/player_{i}.png').convert_alpha()
            img = pg.transform.scale(img, (self.width, self.height))
            frames.append(img)
        return frames

    def _update_animation(self):
        self.anim_timer += 1
        if self.anim_timer >= ANIM_SPEED:
            self.anim_timer = 0
            self.anim_index = (self.anim_index + 1) % len(self.sprites_run)

    def _get_current_sprite(self):
        # Parado: sem movimento horizontal e no chão
        if self.vel_x == 0 and self.on_ground:
            return self.sprite_idle

        # No ar: congela no frame atual (sem ciclar)
        if not self.on_ground:
            return self.sprites_run[self.anim_index]

        # Correndo: anima normalmente
        self._update_animation()
        return self.sprites_run[self.anim_index]

    def handle_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel_x = -4
            self.facing_right = False
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel_x = 4
            self.facing_right = True
        else:
            self.vel_x = 0

    def request_jump(self):
        self.jump_buffer_timer = JUMP_BUFFER_FRAMES

    def try_jump(self):
        can_jump = self.on_ground or self.coyote_timer > 0
        wants_jump = self.jump_buffer_timer > 0
        if can_jump and wants_jump:
            self.vel_y = self.jump_force
            self.on_ground = False
            self.coyote_timer = 0
            self.jump_buffer_timer = 0

    def kill_enemy_bounce(self):
        self.vel_y = -8
        self.on_ground = False

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

        if was_on_ground and not self.on_ground:
            self.coyote_timer = COYOTE_FRAMES

    def take_damage(self):
        if self.invincible_timer > 0:
            return
        self.lives -= 1
        self.invincible_timer = INVINCIBLE_FRAMES
        if self.lives <= 0:
            self.alive = False

    def respawn(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.vel_x = 0
        self.invincible_timer = 0

    def is_fallen(self):
        return self.y > WIN_HEIGHT + 50

    def update_timers(self):
        if self.coyote_timer > 0:
            self.coyote_timer -= 1
        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= 1
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def update(self, platforms=None):
        self.handle_input()
        self.apply_gravity()

        self.x += self.vel_x
        self.y += self.vel_y

        if platforms:
            self.check_platform_collision(platforms)

        self.try_jump()
        self.update_timers()

    def draw(self):
        # Não desenha durante invencibilidade (piscar)
        if self.invincible_timer > 0 and (self.invincible_timer // 4) % 2 == 0:
            return

        sprite = self._get_current_sprite()

        # Espelha o sprite se estiver indo para a esquerda
        if not self.facing_right:
            sprite = pg.transform.flip(sprite, True, False)

        self.window.blit(sprite, (self.x, self.y))

    def get_rect(self):
        return pg.Rect(self.x, self.y, self.width, self.height)
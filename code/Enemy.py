import pygame
import math
from code.Entity import Entity
from code.resource_path import resource_path


ENEMY_HP = 20


class Enemy(Entity):

    FRAME_SIZE = 32
    ANIMATION_SPEED = 8

    def __init__(self, position: tuple):
        super().__init__('3 Dungeon Enemies/2/D_Walk', position)

        self.speed = 1.5
        self.frame_index = 0
        self.frame_timer = 0
        self.hp = ENEMY_HP
        self.max_hp = ENEMY_HP
        self.damage_inflate = -50  # default hitbox reduction
        self.took_damage = False

        # Float position for smooth movement
        self.x = float(position[0])
        self.y = float(position[1])

        self.sprites = {
            'walk_down': self._load_frames('D_Walk', 6),
            'walk_up':   self._load_frames('U_Walk', 6),
            'walk_side': self._load_frames('S_Walk', 6),
        }

        self.current_anim = 'walk_down'
        self.surf = self.sprites[self.current_anim][0]
        self.rect = self.surf.get_rect(center=position)
        self.flip = False

    def _load_frames(self, name: str, count: int):
        sheet = pygame.image.load(resource_path(f'./assets/3 Dungeon Enemies/2/{name}.png')).convert_alpha()
        frames = []
        for i in range(count):
            frame = sheet.subsurface(pygame.Rect(i * self.FRAME_SIZE, 0, self.FRAME_SIZE, self.FRAME_SIZE))
            frames.append(pygame.transform.scale(frame, (64, 64)))
        return frames

    def take_damage(self, amount: int):
        self.hp -= amount
        self.took_damage = True

    def is_alive(self):
        return self.hp > 0

    def move(self, target_rect: pygame.Rect = None):
        if target_rect is None:
            return

        dx = target_rect.centerx - self.x
        dy = target_rect.centery - self.y
        dist = math.hypot(dx, dy)

        if dist != 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

        # Sync rect with float position
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        abs_dx = abs(target_rect.centerx - self.x)
        abs_dy = abs(target_rect.centery - self.y)

        if abs_dy >= abs_dx:
            if target_rect.centery > self.y:
                self.current_anim = 'walk_down'
                self.flip = False
            else:
                self.current_anim = 'walk_up'
                self.flip = False
        else:
            self.current_anim = 'walk_side'
            self.flip = target_rect.centerx < self.x

        self.frame_timer += 1
        if self.frame_timer >= self.ANIMATION_SPEED:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.sprites[self.current_anim])

        frame = self.sprites[self.current_anim][self.frame_index]
        self.surf = pygame.transform.flip(frame, self.flip, False)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, self.rect)
        # HP bar
        if self.took_damage:
            bar_width = self.rect.width - 20
            bar_height = 3
            bar_x = self.rect.x + 10
            bar_y = self.rect.y - 1
            hp_ratio = self.hp / self.max_hp
            pygame.draw.rect(screen, (80, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (220, 50, 50), (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))

class TankEnemy(Enemy):

    def __init__(self, position: tuple):
        super().__init__(position)
        self.hp = ENEMY_HP * 3
        self.speed = 0.6
        self.max_hp = ENEMY_HP * 3
        self.damage_inflate = -70  # larger hitbox reduction for tank

        self.sprites = {
            'walk_down': self._load_frames_scaled('D_Walk', 6),
            'walk_up':   self._load_frames_scaled('U_Walk', 6),
            'walk_side': self._load_frames_scaled('S_Walk', 6),
        }

        self.surf = self.sprites[self.current_anim][0]
        self.rect = self.surf.get_rect(center=position)

    def _load_frames_scaled(self, name: str, count: int):
        sheet = pygame.image.load(resource_path(f'assets/3 Dungeon Enemies/2/{name}.png')).convert_alpha()
        frames = []
        for i in range(count):
            frame = sheet.subsurface(pygame.Rect(i * self.FRAME_SIZE, 0, self.FRAME_SIZE, self.FRAME_SIZE))
            frames.append(pygame.transform.scale(frame, (96, 96)))
        return frames
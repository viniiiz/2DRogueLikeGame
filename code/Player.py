import pygame
from code.Entity import Entity
from code.Const import WIN_WIDTH, WIN_HEIGHT, PLAYER_MAX_HP


class Player(Entity):

    FRAME_SIZE = 32
    ANIMATION_SPEED = 8  # game frames per sprite frame
    INVINCIBILITY_FRAMES = 60  # frames of invincibility after taking damage

    def __init__(self, position: tuple):
        super().__init__('1 Characters/1/U_Idle', position)

        self.speed = 3
        self.frame_index = 0
        self.frame_timer = 0
        self.hp = PLAYER_MAX_HP
        self.invincible_timer = 0  # invincibility frames after being hit

        # Load all spritesheets
        self.sprites = {
            'idle':      self._load_frames('U_Idle', 4),
            'walk_up':   self._load_frames('U_Walk', 6),
            'walk_down': self._load_frames('D_Walk', 6),
        }

        self.current_anim = 'idle'
        self.surf = self.sprites[self.current_anim][0]
        self.rect = self.surf.get_rect(center=position)

    def _load_frames(self, name: str, count: int):
        sheet = pygame.image.load(f'./assets/1 Characters/1/{name}.png').convert_alpha()
        frames = []
        for i in range(count):
            frame = sheet.subsurface(pygame.Rect(i * self.FRAME_SIZE, 0, self.FRAME_SIZE, self.FRAME_SIZE))
            frames.append(pygame.transform.scale(frame, (64, 64)))  # scale 2x
        return frames

    def take_damage(self):
        # Only take damage if not currently invincible
        if self.invincible_timer == 0:
            self.hp -= 1
            self.invincible_timer = self.INVINCIBILITY_FRAMES

    def is_alive(self):
        return self.hp > 0

    def move(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        prev_anim = self.current_anim

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed

        # Set animation based on movement direction
        if dy < 0:
            self.current_anim = 'walk_up'
        elif dy > 0:
            self.current_anim = 'walk_down'
        elif dx != 0:
            self.current_anim = 'walk_up'  # no side sprite available
        else:
            self.current_anim = 'idle'

        # Reset frame index when animation changes
        if self.current_anim != prev_anim:
            self.frame_index = 0
            self.frame_timer = 0

        # Clamp player to screen bounds
        self.rect.x = max(0, min(WIN_WIDTH - self.rect.width, self.rect.x + dx))
        self.rect.y = max(0, min(WIN_HEIGHT - self.rect.height, self.rect.y + dy))

        # Advance animation frame
        self.frame_timer += 1
        if self.frame_timer >= self.ANIMATION_SPEED:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.sprites[self.current_anim])

        self.surf = self.sprites[self.current_anim][self.frame_index]

        # Tick down invincibility
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def draw(self, screen: pygame.Surface):
        # Blink while invincible
        if self.invincible_timer == 0 or self.invincible_timer % 6 < 3:
            screen.blit(self.surf, self.rect)
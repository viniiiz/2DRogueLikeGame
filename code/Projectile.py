import pygame
import math


class Projectile:

    SPEED = 6
    SCALE = (22, 6)

    def __init__(self, origin: pygame.Rect, target: pygame.Rect):
        base_surf = pygame.image.load('./assets/1 Characters/Other/Arrow.png').convert_alpha()
        base_surf = pygame.transform.scale(base_surf, self.SCALE)

        # Calculate direction toward target
        dx = target.centerx - origin.centerx
        dy = target.centery - origin.centery
        dist = math.hypot(dx, dy)
        self.vel_x = (dx / dist) * self.SPEED
        self.vel_y = (dy / dist) * self.SPEED

        # Rotate sprite to face direction
        angle = -math.degrees(math.atan2(dy, dx))
        self.surf = pygame.transform.rotate(base_surf, angle)

        # Use a small fixed hitbox instead of the rotated rect
        self.rect = pygame.Rect(0, 0, 2, 2)
        self.rect.center = origin.center

        # Use float position for smooth movement
        self.x = float(origin.centerx)
        self.y = float(origin.centery)

        self.active = True

    def update(self, screen_width: int, screen_height: int):
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.center = (int(self.x), int(self.y))

        # Deactivate if out of screen
        if (self.rect.right < 0 or self.rect.left > screen_width or
                self.rect.bottom < 0 or self.rect.top > screen_height):
            self.active = False

    def draw(self, screen: pygame.Surface):
        draw_rect = self.surf.get_rect(center=self.rect.center)
        screen.blit(self.surf, draw_rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)  # debug hitbox
    
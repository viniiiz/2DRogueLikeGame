import pygame
from code.Const import COLOR_RED, COLOR_DARK_RED, PLAYER_MAX_HP


class HUD:

    HEART_SIZE = 28
    HEART_MARGIN = 10
    HEART_X = 20
    HEART_Y = 20

    def __init__(self):
        pass

    def _draw_heart(self, screen: pygame.Surface, x: int, y: int, filled: bool):
        color = COLOR_RED if filled else COLOR_DARK_RED
        s = self.HEART_SIZE

        # Two circles on top
        pygame.draw.circle(screen, color, (x + s // 4,     y + s // 4), s // 4)
        pygame.draw.circle(screen, color, (x + 3 * s // 4, y + s // 4), s // 4)

        # Triangle pointing down
        points = [
            (x,         y + s // 4),
            (x + s,     y + s // 4),
            (x + s // 2, y + s),
        ]
        pygame.draw.polygon(screen, color, points)

    def draw(self, screen: pygame.Surface, current_hp: int):
        for i in range(PLAYER_MAX_HP):
            x = self.HEART_X + i * (self.HEART_SIZE + self.HEART_MARGIN)
            filled = i < current_hp
            self._draw_heart(screen, x, self.HEART_Y, filled)
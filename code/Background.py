import pygame
from code.Entity import Entity

class Background(Entity):

    def __init__(self, position: tuple, screen_width: int, screen_height: int):
        self.name = "background"
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 0

        self.surf = pygame.Surface((screen_width, screen_height))
        self.surf.fill((110, 110, 110))  # cinza médio (chão visto de cima)

        self.rect = self.surf.get_rect(left=position[0], top=position[1])

    def move(self):
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, self.rect)
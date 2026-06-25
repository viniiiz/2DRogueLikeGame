import pygame
from code.Entity import Entity
from code.Background import Background
from code.Const import WIN_WIDTH, WIN_HEIGHT


class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []

        # Adiciona o background à lista de entidades
        self.entity_list.append(Background((0, 0), WIN_WIDTH, WIN_HEIGHT))

    def run_level(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # ESC volta ao menu
                        return "MENU"

            # Desenha todas as entidades
            for entity in self.entity_list:
                entity.draw(self.window)

            pygame.display.flip()
            clock.tick(60)
import sys

from code.Const import COLOR_WHITE, COLOR_YELLOW, MENU_OPTION, WIN_WIDTH
from code.resource_path import resource_path

import pygame


class Menu:

    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load(resource_path('assets/menuBG1.png'))
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0
        while True:
            # Draw background
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, "Rogue Like Game", COLOR_YELLOW, ((WIN_WIDTH / 2), 120))

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(30, MENU_OPTION[i], COLOR_YELLOW, ((WIN_WIDTH / 2), 250 + i * 100))
                else:
                    self.menu_text(30, MENU_OPTION[i], COLOR_WHITE, ((WIN_WIDTH / 2), 250 + i * 100))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN:
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf = text_font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
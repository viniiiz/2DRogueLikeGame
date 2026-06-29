from code.Const import COLOR_WHITE, COLOR_YELLOW, MENU_OPTION
from tkinter.font import Font

import pygame

from code.Const import WIN_WIDTH


class Menu:

    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('assets/menuBG1.png')
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self, ):
        menu_option = 0
        #pygame.mixer_music.set_volume(0.3)  # Set the volume (0.0 to 1.0)
        #pygame.mixer_music.load('./assets/8bittypemusic1.mp3')
        #pygame.mixer_music.play(-1)  # Loop the music
        while True:
            # DRAW IMAGES
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(50, "Rogue Like Game", COLOR_YELLOW, ((WIN_WIDTH / 2), 120))
            
            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(30, MENU_OPTION[i], COLOR_YELLOW, ((WIN_WIDTH / 2), 250 + i * 100))
                else:
                    self.menu_text(30, MENU_OPTION[i], COLOR_WHITE, ((WIN_WIDTH / 2), 250 + i * 100))
            pygame.display.flip()
        

            # Check for all events
            for event in pygame.event.get():
                # If the event is the quit event, exit the loop
                if event.type == pygame.QUIT:
                    pygame.quit() #Close Window
                    quit() #Exit Program
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s: #DOWNKEYS
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0 
                    if event.key == pygame.K_UP or event.key == pygame.K_w: #UP KEYS
                        if menu_option > 0:
                            menu_option -= 1        
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN: #ENTER KEY
                        return MENU_OPTION[menu_option]
                        
                        
            

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: pygame.Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: pygame.Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
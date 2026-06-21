import pygame

from code.Menu import Menu
from code.Const import WIN_HEIGHT, WIN_WIDTH

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=( WIN_WIDTH, WIN_HEIGHT))


    def run(self):


        while True:
            menu = Menu(self.window)
            menu.run()
            pass


            
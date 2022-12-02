import pygame

from typing import List

from common.constants import *
from ui.main_menu import MainMenu


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 50)

        self.bg = pygame.image.load("./resources/textures/background.jpg")

        self.screens = {""}

    def start(self):
        menu = MainMenu(self.screen, self.clock, self.bg, self.font,
                        self.game)
        menu.startup_screen()

    def game(self, company_name: str):
        print(company_name)


import random

import pygame
import json

from typing import List

from common.constants import *
from ui.main_menu import MainMenu
from ui.ships import ShipShop

from models import Company, ShipBase


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 50)

        self.bg = pygame.image.load("./resources/textures/background.jpg", "background")

        self.screens = {}

        self.ships: List[ShipBase] = []
        self.load_ships()

    def start(self):
        menu = MainMenu(self.screen, self.clock, self.bg, self.font,
                        self.game)
        menu.startup_screen()

    def load_ships(self, file_name: str = r"./resources/data/ships.json"):
        with open(file_name, "r") as file:
            data = json.load(file)
        for ship in data:
            name = random.choice(SHIP_NAMES)
            while name in [s.name for s in self.ships]:
                name = random.choice(SHIP_NAMES)
            self.ships.append(ShipBase(ship, name, data[ship]["price"], data[ship]["capacity"]))

    def game(self, company_name: str):
        comp = Company(company_name)
        self.screens["ships"] = ShipShop(comp, self.ships, self.bg, self.screen, self.clock)
        self.screens["ships"].startup_screen()


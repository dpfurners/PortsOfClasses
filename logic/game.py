import random

import pygame
import json

from typing import List

from common.constants import *
from ui.main_menu import MainMenu
from ui.ships import ShipShop
from ui.overview import OverviewScreen
from ui.harbor import HarborScreen

from models import Company, ShipBase, HarborBase


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
        self.harbors: List[HarborBase] = []
        self.load_ships()
        self.load_harbors()

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
            pic = pygame.image.load(data[ship]["picture"])
            self.ships.append(ShipBase(ship, name, data[ship]["price"], data[ship]["capacity"], pic))

    def load_harbors(self, file_name: str = r"./resources/data/harbors.json"):
        with open(file_name, "r") as file:
            data = json.load(file)
        for harbor in data:
            pic = pygame.image.load(data[harbor]["picture"])
            self.harbors.append(HarborBase(harbor, data[harbor]["description"], data[harbor]["position"], data[harbor]["capacity"], pic))

    def setup_screens(self, company: Company):
        self.screens["ships"]: ShipShop = ShipShop(company, self.ships, self.bg, self.screen, self.clock)
        self.screens["harbors"]: HarborScreen = HarborScreen(company, self.bg, self.screen, self.clock, self.harbors)
        self.screens["overview"]: OverviewScreen = OverviewScreen(company, self.screen, self.clock, self.screens["ships"].startup_screen)

        # Add Additional data after initializing every Screen
        self.screens["ships"].back_action = self.screens["overview"].startup_screen
        self.screens["harbors"].overview_action = self.screens["overview"].startup_screen

        self.screens["overview"].harbor_overview = self.screens["harbors"]

    def game(self, company_name: str):
        comp = Company(company_name)
        print(self.harbors)
        self.setup_screens(comp)
        self.screens["ships"].startup_screen()



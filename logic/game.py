import random
import datetime
import pygame
import json

from typing import List

from common.constants import *
from ui.main_menu import MainMenu
from ui.ships import ShipShop, ShipDepot
from ui.overview import OverviewScreen
from ui.harbor import HarborScreen
from ui.contracts import ContractScreen, ContractOverview

from models import Company, ShipBase, HarborBase, ContractBase


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 50)

        self.bg = pygame.image.load("./resources/textures/background.jpg", "background")

        self.company: Company | None = None

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
            self.harbors.append(HarborBase(harbor, data[harbor]["description"], data[harbor]["country"], data[harbor]["position"], data[harbor]["capacity"], pic))

    def load_contracts(self, min_pricing: int = 1, max_pricing: int = 100):
        for harbor in self.harbors:
            for i in range(random.randint(2, 9)):
                destination = random.choice(self.harbors)
                while destination == harbor:
                    destination = random.choice(self.harbors)
                pricing = random.randint(min_pricing, max_pricing) * 100
                ship_capacities = [ship.capacity for ship in self.company.ships]
                amount = int(random.randint(min(ship_capacities)/10, max(ship_capacities)) + max(ship_capacities)/10)
                time = datetime.time(minute=random.randint(1, 3), second=random.randint(0, 59))
                harbor.available_contracts.append(ContractBase(harbor, destination, pricing, amount, "Rice", time))

    def setup_screens(self):
        self.screens["ships"]: ShipShop = ShipShop(self.company, self.ships, self.bg, self.screen, self.clock, self.load_contracts)
        self.screens["ship_depot"]: ShipDepot = ShipDepot(self.company, self.bg, self.screen, self.clock)
        self.screens["harbors"]: HarborScreen = HarborScreen(self.company, self.bg, self.screen, self.clock, self.harbors)
        self.screens["overview"]: OverviewScreen = OverviewScreen(self.company, self.screen, self.clock, self.screens["ships"].startup_screen)
        self.screens["contracts"]: ContractScreen = ContractScreen(self.company, self.bg, self.screen, self.clock)
        self.screens["contract_overview"]: ContractOverview = ContractOverview(self.company, self.bg, self.screen, self.clock)

        # Add Additional data after initializing every Screen
        self.screens["ships"].back_action = self.screens["overview"].startup_screen
        self.screens["ship_depot"].back_action = self.screens["overview"].startup_screen
        self.screens["harbors"].overview_action = self.screens["overview"].startup_screen
        self.screens["contract_overview"].back_action = self.screens["overview"].startup_screen
        self.screens["harbors"].contract_action = self.screens["contracts"].display_contract

        self.screens["overview"].harbor_overview = self.screens["harbors"]
        self.screens["overview"].ship_depot_action = self.screens["ship_depot"].startup_screen
        self.screens["overview"].contract_overview = self.screens["contract_overview"].startup_screen
        self.screens["contracts"].back_action = self.screens["harbors"].startup_screen
        self.screens["contracts"].select_ship_action = self.screens["ship_depot"].startup_screen
        self.screens["contracts"].harbors = self.harbors

    def game(self, company_name: str):
        self.company = Company(company_name)
        self.setup_screens()
        self.screens["ships"].startup_screen()



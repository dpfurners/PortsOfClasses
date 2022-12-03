import pygame
import sys
import random
from math import floor

from typing import List

from ui.screen import Screen
from models import Company, ShipBase, ContractBase
from common.helpers import draw_text
from common.colors import FONT_DARK, WHITE
from common.constants import SHIP_NAMES


class ContractScreen(Screen):
    def __init__(self, company: Company, bg, screen: pygame.Surface, clock: pygame.time.Clock):
        super().__init__("ship_screen", screen, clock)
        self.bg = bg
        self.company = company
        self.back_action = None
        self.contract: ContractBase | None = None
        self.fields = {}

    def display_contract(self, contract: ContractBase):
        self.contract = contract
        self.startup_screen()

    def select_ship(self):
        pass

    def startup_screen(self):
        click = False
        while 1:
            self.fields = {}
            self.screen.blit(self.bg, (0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(50, 50, 900, 600), 0, 5)

            draw_text("Contract", FONT_DARK, self.screen, 75, 75, 50)
            draw_text(f"Balance: {self.company.get_current_money:_}$", FONT_DARK, self.screen, 500, 75, 25)
            draw_text(f"Max. Capacity: {max([ship.capacity for ship in self.company.ships if ship.contract is None]):_}", FONT_DARK, self.screen, 500, 100, 25)

            pygame.draw.rect(self.screen, (0, 161, 255), pygame.Rect(75, 125, 850, 500), 0, 5)
            draw_text(f"{self.contract.source.name} -> {self.contract.destination.name}", FONT_DARK, self.screen, 80, 130, 50)
            draw_text(f"Quantity: {self.contract.quantity:_}", FONT_DARK, self.screen, 85, 170, 35)
            draw_text(f"Pricing: {self.contract.total:_}$", FONT_DARK, self.screen, 85, 200, 35)
            draw_text(f"Goods: {self.contract.goods}", FONT_DARK, self.screen, 85, 230, 35)
            draw_text(f"Time: {self.contract.time.strftime('%M:%S')}", FONT_DARK, self.screen, 85, 260, 35)

            select_ship = pygame.Rect(820, 505, 50, 50)
            self.screen.blit(pygame.image.load("./resources/textures/sign.png"), (820, 505))
            self.fields["select_ship"] = [0, select_ship]

            go_on = pygame.Rect(864, 65, 50, 50)
            self.screen.blit(pygame.image.load("./resources/textures/cross.png"), (864, 65))
            # pygame.draw.rect(self.screen, (255, 161, 0), go_on, 0, 2)
            self.fields["go_on"] = [0, go_on]

            mx, my = pygame.mouse.get_pos()
            for field in self.fields:
                if self.fields[field][1].collidepoint((mx, my)):
                    if click:
                        if field == "go_on":
                            self.back_action()
                        elif field == "select_ship":
                            self.select_ship()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                if event.type == pygame.MOUSEBUTTONUP:
                    click = False

            pygame.display.update()
            self.clock.tick(30)

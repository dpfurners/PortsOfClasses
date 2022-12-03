import pygame
import sys
import random
import datetime
from math import floor

from typing import List

from ui.screen import Screen
from models import Company, ShipBase, ContractBase
from common.helpers import draw_text, new_button
from common.colors import FONT_DARK, WHITE
from common.constants import SHIP_NAMES, SHIPPING_ENDED_EVENT


class ContractScreen(Screen):
    def __init__(self, company: Company, bg, screen: pygame.Surface, clock: pygame.time.Clock):
        super().__init__("contract_screen", screen, clock)
        self.bg = bg
        self.company = company
        self.back_action = None
        self.select_ship_action = None
        self.harbors = None
        self.contract: ContractBase | None = None
        self.fields = {}

    def display_contract(self, contract: ContractBase):
        self.contract = contract
        self.startup_screen()

    def select_ship(self):
        ship = self.select_ship_action(True)
        ship.contract = self.contract
        ship.contract.source.available_contracts.remove(ship.contract)
        return ship

    def startup_screen(self):
        click = False
        while 1:
            self.fields = {}
            self.screen.blit(self.bg, (0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(50, 50, 900, 600), 0, 5)

            draw_text("Contract", FONT_DARK, self.screen, 75, 75, 50)
            draw_text(f"Balance: {self.company.get_current_money:_}$", FONT_DARK, self.screen, 500, 75, 25)
            try:
                draw_text(f"Max. Capacity: {max([ship.capacity for ship in self.company.ships if ship.contract is None]):_}", FONT_DARK, self.screen, 500, 100, 25)
            except ValueError:
                draw_text(f"Max. Capacity: 0", FONT_DARK, self.screen, 500, 100, 25)
            pygame.draw.rect(self.screen, (0, 161, 255), pygame.Rect(75, 125, 850, 500), 0, 5)
            draw_text(f"{self.contract.source.name} -> {self.contract.destination.name}", FONT_DARK, self.screen, 80, 130, 50)
            draw_text(f"Quantity: {self.contract.quantity:_}", FONT_DARK, self.screen, 85, 170, 35)
            draw_text(f"Pricing: {self.contract.total:_}$", FONT_DARK, self.screen, 85, 200, 35)
            draw_text(f"Goods: {self.contract.goods}", FONT_DARK, self.screen, 85, 230, 35)
            draw_text(f"Time: {self.contract.time.strftime('%M:%S')}", FONT_DARK, self.screen, 85, 260, 35)

            select_ship = new_button(self.screen, (820, 505), (100, 100), picture="./resources/textures/sign.png")
            self.fields["select_ship"] = [0, select_ship]

            go_on = new_button(self.screen, (864, 65), (50, 50), picture="./resources/textures/cross.png")
            self.fields["go_on"] = [0, go_on]

            mx, my = pygame.mouse.get_pos()
            for field in self.fields:
                if self.fields[field][1].collidepoint((mx, my)):
                    if click:
                        if field == "go_on":
                            self.back_action()
                        elif field == "select_ship":
                            self.select_ship()
                            pygame.time.set_timer(SHIPPING_ENDED_EVENT, self.contract.time.microsecond * 100)
                            self.contract.started = datetime.datetime.now()
                            self.contract = None
                            self.back_action()

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


class ContractOverview(Screen):
    def __init__(self, company: Company, bg, screen: pygame.Surface, clock: pygame.time.Clock):
        super().__init__("contract_overview", screen, clock)
        self.bg = bg
        self.company = company
        self.back_action = None
        self.fields = {}

    def display_running_contracts(self):
        contract_ships = [ship for ship in self.company.ships if ship.contract]
        for index, ship in enumerate(contract_ships):
            x = y = 0
            x = 75
            y = 105 * (floor(index / 2) + 1) + 20
            rect = pygame.Rect(x, y, 420, 100)
            pygame.draw.rect(self.screen, (0, 161, 255), rect, 0, 2)
            draw_text(ship.name, FONT_DARK, self.screen, x + 5, y + 5, 35)  # Display Ship Name
            draw_text(ship.type, FONT_DARK, self.screen, x + 5, y + 30, 20)  # Display Ship Type

            draw_text(f"Capacity: {ship.capacity:_}", FONT_DARK, self.screen, x + 5, y + 50, 30)
            draw_text(f"Price: {ship.price:_}$", FONT_DARK, self.screen, x + 5, y + 72.5, 35)
            if ship.contract.done():
                draw_text("Done", FONT_DARK, self.screen, x + 300, y + 30, 60)
            else:
                draw_text(ship.contract.strfdelta(), FONT_DARK, self.screen, x + 300, y + 30, 60)
            self.fields[ship] = [ship, rect]

    def display_done_contracts(self):
        for index, contract in enumerate(self.company.done_contracts):
            x = y = 0
            x = 500
            y = 105 * (floor(index / 2) + 1) + 20
            rect = pygame.Rect(x, y, 420, 100)
            pygame.draw.rect(self.screen, (0, 161, 255), rect, 0, 2)
            draw_text(f"{contract.source} -> {contract.destination}", FONT_DARK, self.screen, x + 5, y + 5, 35)  # Display Ship Name
            draw_text(f"Total: {contract.total}", FONT_DARK, self.screen, x + 5, y + 30, 20)  # Display Ship Type

            self.fields[contract] = [contract, rect]

    def startup_screen(self):
        run = True
        click = False
        while run:
            self.fields = {}
            self.screen.blit(self.bg, (0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(50, 50, 900, 600), 0, 5)

            draw_text("Contracts", FONT_DARK, self.screen, 75, 75, 50)
            draw_text(f"Balance: {self.company.get_current_money:_}$", FONT_DARK, self.screen, 500, 75, 40)

            self.display_done_contracts()
            self.display_running_contracts()

            back = new_button(self.screen, (864, 65), (50, 50), picture="./resources/textures/cross.png")
            self.fields["back"] = [0, back]

            mx, my = pygame.mouse.get_pos()
            # print(fields)
            for field in self.fields:
                if self.fields[field][1].collidepoint((mx, my)):
                    if click:
                        if field == "back":
                            self.back_action()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                if event.type == pygame.MOUSEBUTTONUP:
                    click = False

            pygame.display.update()
            self.clock.tick(60)

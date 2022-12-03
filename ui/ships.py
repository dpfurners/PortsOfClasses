import pygame
import sys
import random
from math import floor

from typing import List

from ui.screen import Screen
from models import Company, ShipBase
from common.helpers import draw_text, new_button
from common.colors import FONT_DARK, WHITE
from common.constants import SHIP_NAMES


class ShipShop(Screen):
    def __init__(self, company: Company, ships: List[ShipBase], bg, screen: pygame.Surface, clock: pygame.time.Clock, load_contracts):
        super().__init__("ship_screen", screen, clock)
        self.bg = bg
        self.company = company
        self.load_contracts = load_contracts
        self.ships = ships
        self.back_action = None

        self.fields: dict = {}

        self.inspect: ShipBase | None = None

    def display_available_ships(self):
        if len(self.ships) <= 10:
            for index, ship in enumerate(self.ships):
                x = y = 0
                x = 75 if (index + 1) % 2 == 1 else 500
                y = 105 * (floor(index/2) + 1) + 20
                rect = new_button(self.screen, (x, y), (420, 100), color=(0, 161, 255))
                draw_text(ship.name, FONT_DARK, self.screen, x+5, y+5, 35)      # Display Ship Name
                draw_text(ship.type, FONT_DARK, self.screen, x+5, y+30, 20)   # Display Ship Type

                draw_text(f"Capacity: {ship.capacity:_}", FONT_DARK, self.screen, x+5, y+50, 30)
                draw_text(f"Price: {ship.price:_}$", FONT_DARK, self.screen, x+5, y+72.5, 35)
                self.fields[ship] = [ship, rect]

    def display_ship(self, ship):
        pygame.draw.rect(self.screen, (0, 161, 255), pygame.Rect(75, 125, 845, 520), 0, 3)

        back = new_button(self.screen, (864, 65), (50, 50), picture="./resources/textures/cross.png")
        self.fields["back"] = [0, back]

        draw_text(ship.name, FONT_DARK, self.screen, 80, 130, 60)
        draw_text(ship.type, FONT_DARK, self.screen, 85, 170, 40)

        self.screen.blit(ship.picture, (100, 200))

        draw_text(f"Capacity: {ship.capacity:_}", FONT_DARK, self.screen, 85, 570, 40)
        draw_text(f"Price: {ship.price:_}$", FONT_DARK, self.screen, 85, 610, 40)

        buy = new_button(self.screen, (720, 450), (200, 200), picture="./resources/textures/buy.png")
        self.fields["buy"] = [0, buy]

    def startup_screen(self):
        run = True
        click = False
        while run:
            self.fields = {}
            self.screen.blit(self.bg, (0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(50, 50, 900, 600), 0, 5)

            draw_text("Boat-Sales", FONT_DARK, self.screen, 75, 75, 50)
            draw_text(f"Balance: {self.company.get_current_money:_}$", FONT_DARK, self.screen, 500, 75, 40)

            if isinstance(self.inspect, ShipBase):
                self.display_ship(self.inspect)
            else:
                self.display_available_ships()

            if self.company.ships:
                go_on = new_button(self.screen, (864, 65), (50, 50), picture="./resources/textures/cross.png")
                self.fields["go_on"] = [0, go_on]

            mx, my = pygame.mouse.get_pos()
            # print(fields)
            for field in self.fields:
                if self.fields[field][1].collidepoint((mx, my)):
                    if click:
                        if field == "back":
                            self.inspect = None
                            pygame.time.wait(100)
                        elif field == "buy":
                            if self.company.buy_ship(self.inspect) is True:
                                self.load_contracts()
                                name = random.choice(SHIP_NAMES)
                                while name in [s.name for s in self.ships]:
                                    name = random.choice(SHIP_NAMES)
                                self.ships[self.ships.index(self.inspect)] = ShipBase(self.inspect.type, name, self.inspect.price, self.inspect.capacity, self.inspect.picture)
                                self.inspect = None
                                self.fields.pop(field)
                                break
                            pygame.time.wait(100)
                        elif field == "go_on":
                            self.back_action()
                        else:
                            self.inspect = self.fields[field][0]
                            pygame.time.wait(100)

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


class ShipDepot(Screen):
    def __init__(self, company: Company, bg, screen: pygame.Surface, clock: pygame.time.Clock):
        super().__init__("own_ship_screen", screen, clock)
        self.bg = bg
        self.company = company
        self.back_action = None
        self.select: bool = False

        self.fields: dict = {}

        self.inspect: ShipBase | None = None

    def display_owned_ships(self):
        go_on = new_button(self.screen, (864, 65), (50, 50), picture="./resources/textures/cross.png")
        self.fields["go_on"] = [0, go_on]
        if len(self.company.ships) <= 10:
            for index, ship in enumerate(self.company.ships):
                x = y = 0
                x = 75 if (index + 1) % 2 == 1 else 500
                y = 105 * (floor(index/2) + 1) + 20
                rect = pygame.Rect(x, y, 420, 100)
                pygame.draw.rect(self.screen, (0, 161, 255), rect, 0, 2)
                draw_text(ship.name, FONT_DARK, self.screen, x+5, y+5, 35)    # Display Ship Name
                draw_text(ship.type, FONT_DARK, self.screen, x+5, y+30, 20)   # Display Ship Type

                draw_text(f"Capacity: {ship.capacity:_}", FONT_DARK, self.screen, x+5, y+50, 30)
                draw_text(f"Price: {ship.price:_}$", FONT_DARK, self.screen, x+5, y+72.5, 35)
                if ship.contract:
                    if ship.contract.done():
                        draw_text("Done", FONT_DARK, self.screen, x + 300, y + 30, 60)
                    else:
                        draw_text(ship.contract.strfdelta(), FONT_DARK, self.screen, x+300, y+30, 60)
                self.fields[ship] = [ship, rect]

    def display_ship(self, ship: ShipBase):
        pygame.draw.rect(self.screen, (0, 161, 255), pygame.Rect(75, 125, 845, 520), 0, 3)

        back = new_button(self.screen, (864, 65), (50, 50), picture="./resources/textures/cross.png")
        self.fields["back"] = [0, back]

        draw_text(ship.name, FONT_DARK, self.screen, 80, 130, 60)
        draw_text(ship.type, FONT_DARK, self.screen, 85, 170, 40)

        self.screen.blit(ship.picture, (100, 200))

        draw_text(f"Capacity: {ship.capacity:_}", FONT_DARK, self.screen, 85, 570, 40)
        draw_text(f"Price: {ship.price:_}$", FONT_DARK, self.screen, 85, 610, 40)

        sell = new_button(self.screen, (650, 200), (200, 50), color=(255, 161, 0))
        draw_text("Sell", FONT_DARK, self.screen, 655, 210, 50)
        self.fields["sell"] = [0, sell]

        if ship.contract:
            draw_text(f"Contract: {ship.contract.source.name} -> {ship.contract.destination.name}", FONT_DARK, self.screen, 500, 570, 20)
            draw_text(f"Total: {ship.contract.total}", FONT_DARK, self.screen, 500, 590, 15)
            draw_text(f"Quantity: {ship.contract.quantity}", FONT_DARK, self.screen, 500, 600, 15)
            draw_text(f"Time: {ship.contract.time.strftime('%M:%S')}", FONT_DARK, self.screen, 500, 610, 15)

            if ship.contract.done():
                draw_text("Done", FONT_DARK, self.screen, 655, 150, 60)
            else:
                draw_text(ship.contract.strfdelta(), FONT_DARK, self.screen, 655, 150, 60)

            button = new_button(self.screen, (650, 255), (200, 50), color=(255, 161, 0))
            if ship.contract.done():
                draw_text("Claim", FONT_DARK, self.screen, 655, 265, 50)
                self.fields["claim"] = [0, button]
            else:
                draw_text("Cancel", FONT_DARK, self.screen, 655, 265, 50)
                self.fields["cancel"] = [0, button]

        if self.select:
            select = new_button(self.screen, (720, 550), (200, 100), picture="./resources/textures/arrow.png")
            self.fields["select"] = [0, select]

    def startup_screen(self, select: bool = False):
        self.select = select
        run = True

        click = False
        while run:
            self.fields = {}
            self.screen.blit(self.bg, (0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(50, 50, 900, 600), 0, 5)

            draw_text("Boat-Sales", FONT_DARK, self.screen, 75, 75, 50)
            draw_text(f"Balance: {self.company.get_current_money:_}$", FONT_DARK, self.screen, 500, 75, 40)

            if isinstance(self.inspect, ShipBase):
                self.display_ship(self.inspect)
            else:
                self.display_owned_ships()

            mx, my = pygame.mouse.get_pos()
            for field in self.fields:
                if self.fields[field][1].collidepoint((mx, my)):
                    if click:
                        if field == "back":
                            self.inspect = None
                            pygame.time.wait(100)
                        elif field == "select":
                            ship = self.inspect
                            self.inspect = None
                            return ship
                        elif field == "go_on":
                            self.back_action()
                        elif field == "claim":
                            self.company.done_contracts.append(self.inspect.contract)
                            self.inspect.contract = None
                            self.inspect = None
                            pygame.time.wait(100)
                        elif field == "cancel":
                            self.inspect.contract = None
                            self.inspect = None
                        elif field == "sell":
                            self.company.sell_ship(self.inspect)
                            self.inspect = None
                            pygame.time.wait(100)
                        else:
                            self.inspect = self.fields[field][0]
                            pygame.time.wait(100)

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

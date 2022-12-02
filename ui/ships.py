import pygame
import sys
from math import floor

from typing import List

from ui.screen import Screen
from models import Company, ShipBase
from common.helpers import draw_text
from common.colors import FONT_DARK, WHITE


class ShipShop(Screen):
    def __init__(self, company: Company, ships: List[ShipBase], bg, screen: pygame.Surface, clock: pygame.time.Clock):
        super().__init__("ship_screen", screen, clock)
        self.bg = bg
        self.company = company
        self.ships = ships

        self.inspect: ShipBase | None = None

    def display_available_ships(self):
        fields = {}
        if len(self.ships) <= 10:
            for index, ship in enumerate(self.ships):
                x = y = 0
                x = 75 if (index + 1) % 2 == 1 else 500
                y = 105 * (floor(index/2) + 1) + 20
                rect = pygame.Rect(x, y, 420, 100)
                pygame.draw.rect(self.screen, (0, 161, 255), rect, 0, 2)
                draw_text(ship.name, FONT_DARK, self.screen, x+5, y+5, 35)      # Display Ship Name
                draw_text(ship.type, FONT_DARK, self.screen, x+5, y+30, 20)   # Display Ship Type

                draw_text(f"Capacity: {ship.capacity:_}", FONT_DARK, self.screen, x+5, y+50, 30)
                draw_text(f"Price: {ship.price:_}$", FONT_DARK, self.screen, x+5, y+72.5, 35)
                fields[ship] = [ship, rect]
        return fields

    def display_ship(self, ship):
        fields = {}
        pygame.draw.rect(self.screen, (0, 161, 255), pygame.Rect(75, 125, 845, 520), 0, 3)

        back = pygame.Rect(864, 130, 50, 50)
        # pygame.draw.rect(self.screen, (255, 161, 0), back, 0, 3)
        self.screen.blit(pygame.image.load("./resources/textures/cross.png"), (864, 130))
        fields["back"] = [0, back]

        draw_text(ship.name, FONT_DARK, self.screen, 80, 130, 60)
        draw_text(ship.type, FONT_DARK, self.screen, 85, 170, 40)

        draw_text(f"Capacity: {ship.capacity:_}", FONT_DARK, self.screen, 85, 570, 40)
        draw_text(f"Price: {ship.price:_}$", FONT_DARK, self.screen, 85, 610, 40)

        buy = pygame.Rect(720, 450, 200, 200)
        self.screen.blit(pygame.image.load("./resources/textures/buy.png"), (720, 450))
        # pygame.draw.rect(self.screen, (255, 161, 0), buy, 0, 3)
        fields["buy"] = [0, buy]
        return fields

    def startup_screen(self):
        run = True
        fields = {}
        click = False
        while run:
            self.screen.blit(self.bg, (0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(50, 50, 900, 600), 0, 5)

            draw_text("Boat-Sales", FONT_DARK, self.screen, 75, 75, 50)
            draw_text(f"Balance: {self.company.get_current_money:_}$", FONT_DARK, self.screen, 500, 75, 50)
            if isinstance(self.inspect, ShipBase):
                fields = self.display_ship(self.inspect)
            else:
                fields = self.display_available_ships()
            mx, my = pygame.mouse.get_pos()
            for field in fields:
                if fields[field][1].collidepoint((mx, my)):
                    if click:
                        if field == "back":
                            self.inspect = None
                            pygame.time.wait(100)
                        elif field == "buy":
                            self.company.buy_ship(self.inspect)
                            self.inspect = None
                            pygame.time.wait(100)
                        else:
                            self.inspect = fields[field][0]
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

